import scrapy
import execjs

class QuotesSpider(scrapy.Spider):
  name = "quotes"
  jsfun = None

  def start_requests(self):
    urls = [
      'https://www.manhuabei.com/list/click/?page=1',
    ]
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)

  def parse(self, response):
    page = response.url.split("/")[-2]
    filename = f'quotes-{page}.html'
    list_comic = response.css('.list-comic')
    # print(list_comic)

    lock = False

    for list_comic_item in list_comic:
      if lock == False:
        lock = True
        # 封面图
        cover_src = list_comic_item.css('.comic_img img::attr(src)').get()
        # 详情地址
        comic_href = list_comic_item.css('.comic_img::attr(href)').get()
        # print(cover_src)
        # print(comic_href)

        yield scrapy.Request(url=comic_href, callback=self.comicParse)

    # if self.jsfun is None:
    
    #   with open('crypto.js') as f:
    #     jsdata = f.read()
    #     f.close()

    #   self.jsfun = execjs.compile(jsdata)

    # chapterImages = "kRij9OUITN7t1z3+z94zByI2A3QpIRkKaudQ1MoB5/Ddswec4uYgk9GNuU4fpwvLrlFKA7evIq1tVHnl315R4Dk6OS1ifOG0J9WFsOh/1V8LoVzpNm7pmSotdeeT3SKxu1lE2fVvlzMD7TNfKnYefeb/6uxinaj7SAZKAH5wPfLGo25/DcYTybatHaZy+KYwCMarcbVbtQ0DQYv0Z9dmNEXeXrElujpSxBE+q8ctrPW7ei3FbvD4WrVWLffr04er55ChfX9ZZ4v778cpDx98/f1dknlJCWjBDexM+YFHa+0L8XS21vuXMuqC3SK7Jtgou3t+Nf0yKfd7Ywmc7VAYF7f+c5/w5tbEJAExOkIkTk8KZHnkUr4sbbausyjg4JTQ2UG6ObqON2kh57yyHZ7zRcM8Bgotjf6EFG2zxaQ98V/EJqhK53CzhQDwtgE2s4W1M/yhYcx1FCVlg6Vk3+kkjHESHR2FA1Z5nzCWls3zFsRz8hmSMakW3k/847Iu4N1I9gdNF3puS/cCw/i2XrVr/Q06CdLxD7VVwRJ3sYIB3WFEp5BjxNZ7xsHQdAdmzCcU+eGo1e8KJAQTFC2FrAzv9jXMRJmZv8Am7ew5A9RIXSCFeXcZ0ZbeK394iQnmEV62M+3rmXaQIv4RXFoDLLByqHgmRbfa4lGCMxYb1vEdVVAmCaEdCYaWwn/Q+lzQwv8gNA1vnfsvLIcOplhizMDRtwjWVDvTxYGHtCM5Lu6abtw7L68Z+ePR+rzN4f7m65PqXnsD2j2N24wi7HrRtCDfFdlwDmkhOFriBKdFoNXT3m7nTbQM7KjHi7iGM8bDt3rx9AuiBKjpj3R/F/Ci40c3O1lo+qJOIQaGIIHJS1TXYSDVrjQYhBI+7Z8++zXCrMvt"

    # picList = self.jsfun.call('decrypt20180904', chapterImages)

    # print( picList )

    # with open(filename, 'wb') as f:
    #   for pic in picList:
    #     f.write(pic.encode())
    #     f.write('\r\n'.encode())

    # with open(filename, 'wb') as f:
    #   f.write(response.body)
    #   f.close()

    self.log(f'Saved file {filename}')


  def comicParse(self, response):
    page = response.url.split("/")[-2]
    filename = f'quotes-{page}.html'
    # 信息资料
    comic_deCon_liO = response.css('.comic_deCon_liO li')
    # 简介
    comic_deCon_liT = response.css('.comic_deCon_d::text').get()

    li_list = []

    for comic_deCon_liO_index in range(len( comic_deCon_liO )):
      # print( comic_deCon_liO[ comic_deCon_liO_index ] )
      rels = comic_deCon_liO[ comic_deCon_liO_index ].css('a')
      if rels:
        if len( rels ) > 1:
          # print( rels )
          tags = []
          for tag_item_index in range(len(rels)):
            tags.insert( tag_item_index, rels[ tag_item_index ].css('a::text').get() )
          li_list.insert( comic_deCon_liO_index, tags)
        else:
          li_list.insert( comic_deCon_liO_index, comic_deCon_liO[ comic_deCon_liO_index ].css('a::text').get() )
      else:
        li_list.insert( comic_deCon_liO_index, comic_deCon_liO[ comic_deCon_liO_index ].css('::text').get() )

    # ['村田雄介,ONE', '连载中', '少年漫画', ['热血', '战斗'], '日本', '别名： 一击男，ワンパンマン，ONE PUNCH-MAN']
    # print(li_list)


    zj_data = []

    zj_list_title = response.css('.zj_list .c_3')

    for zj_list_title_index in range(len(zj_list_title)):
      temp_data = {}
      temp_data[ 'title' ] = zj_list_title[ zj_list_title_index ].css('::text').get()
      zj_data.insert( zj_list_title_index, temp_data )
      #print( zj_list_title[ zj_list_title_index ].css('::text').get() )

    #print(zj_data)

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

    # 全部章节
    print( zj_data )


    # with open(filename, 'wb') as f:
    #   f.write(response.body)
    #   f.close()


