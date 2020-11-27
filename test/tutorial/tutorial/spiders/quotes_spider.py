import scrapy
import execjs
import re
from tutorial.items import CartoonItem, SectionItem
from tutorial.settings import web_host, decrypt

class QuotesSpider(scrapy.Spider):
  name = "quotes"
  jsfun = None
  Cartoon = CartoonItem()
  page = 1
  amount = 10

  def __init__(self, page = 1, amount = 10):
    self.page = page
    self.amount = amount + page

  def start_requests(self):
    for page in range( self.page, self.amount ):
      url = web_host + '/list/click/?page=' + str(page)
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    list_comic = response.css('.list-comic')[:1]
    for list_comic_item in list_comic:
      cover_src = list_comic_item.css('.comic_img img::attr(src)').get()
      self.Cartoon['cover'] = cover_src
      comic_href = list_comic_item.css('.comic_img::attr(href)').get()
      yield scrapy.Request(url=comic_href, callback=self.comicParse)  

  def comicParse(self, response):
    page = response.url.split("/")[-2]
    self.Cartoon['id'] = page
    self.Cartoon['name'] = response.css('meta[property="og:title"]::attr(content)').get()
    self.Cartoon['des']= response.css('meta[property="og:description"]::attr(content)').get()
    self.Cartoon['updateTime']= response.css('meta[property="og:novel:update_time"]::attr(content)').get()
    comic_deCon_liO = response.css('.comic_deCon_liO li')
    li_list = []
    for comic_deCon_liO_index in range(len( comic_deCon_liO )):
      rels = comic_deCon_liO[ comic_deCon_liO_index ].css('a')
      if rels:
        if len( rels ) > 1:
          tags = []
          for tag_item_index in range(len(rels)):
            tags.insert( tag_item_index, rels[ tag_item_index ].css('a::text').get() )
          li_list.insert( comic_deCon_liO_index, tags)
        else:
          li_list.insert( comic_deCon_liO_index, comic_deCon_liO[ comic_deCon_liO_index ].css('a::text').get() )
      else:
        li_list.insert( comic_deCon_liO_index, comic_deCon_liO[ comic_deCon_liO_index ].css('::text').get() )
    self.Cartoon['author'] = li_list[0]
    self.Cartoon['status'] = li_list[1]
    self.Cartoon['typeTag'] = li_list[2]
    self.Cartoon['classTag'] = li_list[3]
    self.Cartoon['area'] = li_list[4]
    self.Cartoon['alias'] = li_list[5]
    zj_data = []
    zj_list_title = response.css('.zj_list .c_3')
    for zj_list_title_index in range(len(zj_list_title)):
      temp_data = {}
      temp_data[ 'title' ] = zj_list_title[ zj_list_title_index ].css('::text').get()
      zj_data.insert( zj_list_title_index, temp_data )
    zj_list_con = response.css('.zj_list_con')
    for zj_list_con_index in range(len(zj_list_con)):
      fragment = []
      li_a = zj_list_con[ zj_list_con_index ].css('li a')
      for li_a_item in li_a:
        chip = {}
        li_a_title = li_a_item.css('::attr(title)').get()
        li_a_href = li_a_item.css('::attr(href)').get()
        chip[ 'title' ] = li_a_title
        chip[ 'href' ] = li_a_href
        fragment.append( chip )
      zj_data[ zj_list_con_index ]['chip'] = fragment
      self.Cartoon['chapter'] = zj_data
    yield self.Cartoon
    for section in zj_data:
      title = section['title']
      for index,fragment in enumerate(section['chip']):
        name = fragment['title']
        href = fragment['href']
        url = web_host + href
        request = scrapy.Request(url=url, callback=self.sectionParse)
        request.meta['title'] = title
        request.meta['name'] = name
        request.meta['href'] = href
        request.meta['index'] = index
        yield request

  def sectionParse(self, response):
    section = SectionItem()
    section['title'] = response.meta['title']
    section['name'] = response.meta['name']
    section['href'] = response.meta['href']
    section['index'] = response.meta['index']
    
    chapter_image_code = re.search('chapterImages = \".+\";var chapterPath', response.text).group()
    chapter_image_code = re.search('\".+\"', chapter_image_code).group()
    chapter_image_code = chapter_image_code[1:-1]
    if self.jsfun is None:
      with open('crypto.js') as f:
        jsdata = f.read()
        f.close()
      self.jsfun = execjs.compile(jsdata)
    picList = self.jsfun.call(decrypt, chapter_image_code)
    section['picture'] = picList
    yield section
