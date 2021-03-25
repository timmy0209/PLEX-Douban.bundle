# coding=utf-8
import io
import os
import time
import json
import requests
import urllib

DOUBAN_MOVIE_TRAILERURL = 'http://movie.douban.com/subject/%s/trailer'
DOUBAN_MOVIE_SEARCH = "https://www.douban.com/search?cat=1002&q=%s"
DOUBAN_MOVIE_SUBJECT ='http://movie.douban.com/subject/%s/'
DOUBAN_MOVIE_BASE = 'http://movie.douban.com/subject/%s/celebrities'
DOUBAN_SHOW_EPISODES = 'https://movie.douban.com/subject/%s/episode/%s/'
DOUBAN_M_API_SEARCH = "https://m.douban.com/rexxar/api/v2/search?q=%s&type=movie"
DOUBAN_M_API_MOVIE = "https://m.douban.com/rexxar/api/v2/movie/%s/"
DOUBAN_M_API_ROLES = "https://m.douban.com/rexxar/api/v2/movie/%s/celebrities"
DOUBAN_M_API_DUANPING = "https://m.douban.com/rexxar/api/v2/movie/%s/interests?following=1&count=5"
DOUBAN_M_API_TV = "https://m.douban.com/rexxar/api/v2/tv/%s/"
DOUBAN_M_API_TV_ROLES = "https://m.douban.com/rexxar/api/v2/tv/%s/celebrities"
DOUBAN_M_API_TV_DUANPING = "https://m.douban.com/rexxar/api/v2/tv/%s/interests?following=1&count=5"
BAIKE_SEARCH = 'https://baike.baidu.com/search?word=%s+%s&pn=0&rn=0&enc=utf8'

#select largest num
trailer_num = int(Prefs['trailer_num'])    
short_num = int(Prefs['short_num'])
behindthescenes_num = int(Prefs['behindthescenes_num'])
other_num = int(Prefs['other_num'])
ip_url = Prefs['ip_url']
ip_path = Prefs['ip_path']

head={
 'user-Agent':'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'
}

headers = {
          'user-Agent':'Mozilla/5.0 (Linux; Android 11; M2011K2C Build/RKQ1.200928.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.90 Mobile Safari/537.36 hap/1.8/xiaomi com.miui.hybrid/1.8.1.3 com.douban.movie.crywolf/2.1.4 ({"packageName":"com.xiaomi.market","type":"other","extra":{}})',
          'Host':'m.douban.com'
  }

hea = {
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'api.xiaoxiangdaili.com',
        'Accept-Encoding': 'gzip'
    }



def Start():
  pass


# Change pinyin
def multi_get_letter(str_input): 
  if isinstance(str_input, unicode): 
    unicode_str = str_input 
  else: 
    try: 
      unicode_str = str_input.decode('utf8') 
    except: 
      try: 
        unicode_str = str_input.decode('gbk') 
      except: 
        print 'unknown coding'
        return
  return_list = [] 
  #for one_unicode in unicode_str: 
   # return_list.append(single_get_first(one_unicode)) 
  #return return_list
  return single_get_first(unicode_str)

def single_get_first(unicode1): 
  str1 = unicode1.encode('gbk') 
  try:     
    ord(str1) 
    return str1 
  except: 
    asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
    if asc >= -20319 and asc <= -20284: 
      return 'a'
    if asc >= -20283 and asc <= -19776: 
      return 'b'
    if asc >= -19775 and asc <= -19219: 
      return 'c'
    if asc >= -19218 and asc <= -18711: 
      return 'd'
    if asc >= -18710 and asc <= -18527: 
      return 'e'
    if asc >= -18526 and asc <= -18240: 
      return 'f'
    if asc >= -18239 and asc <= -17923: 
      return 'g'
    if asc >= -17922 and asc <= -17418: 
      return 'h'
    if asc >= -17417 and asc <= -16475: 
      return 'j'
    if asc >= -16474 and asc <= -16213: 
      return 'k'
    if asc >= -16212 and asc <= -15641: 
      return 'l'
    if asc >= -15640 and asc <= -15166: 
      return 'm'
    if asc >= -15165 and asc <= -14923: 
      return 'n'
    if asc >= -14922 and asc <= -14915: 
      return 'o'
    if asc >= -14914 and asc <= -14631: 
      return 'p'
    if asc >= -14630 and asc <= -14150: 
      return 'q'
    if asc >= -14149 and asc <= -14091: 
      return 'r'
    if asc >= -14090 and asc <= -13119: 
      return 's'
    if asc >= -13118 and asc <= -12839: 
      return 't'
    if asc >= -12838 and asc <= -12557: 
      return 'w'
    if asc >= -12556 and asc <= -11848: 
      return 'x'
    if asc >= -11847 and asc <= -11056: 
      return 'y'
    if asc >= -11055 and asc <= -10247: 
      return 'z'
    return ''

def pinyin(str_input): 
  b = ''
  if isinstance(str_input, unicode): 
    unicode_str = str_input 
  else: 
    try: 
      unicode_str = str_input.decode('utf8')
    except: 
      try: 
        unicode_str = str_input.decode('gbk')
      except: 
        #print 'unknown coding'
        return  
  for i in range(len(unicode_str)):
    b=b+single_get_first(unicode_str[i])
  return b.upper()


# GET SOME STR
def get_str_btw(s, f, b):
    par = s.partition(f)
    return (par[2].partition(b))[0][:]


# GET BAIKE INFO
def search_baike(title,year):
    url = BAIKE_SEARCH % (title, year)
    content = HTTP.Request(url=url,headers=head)
    html_elem = HTML.ElementFromString(content)
    base_url = html_elem.xpath('.//dl[@class="search-list"]//a/@href')[0]
    if base_url[:4] == "http":
      tv_url = base_url
    else:
      tv_url = "https://baike.baidu.com" + base_url
    return(tv_url)
def get_tvinfo(tv_url):
    content = HTTP.Request(url=tv_url,headers=head)
    html_elem = HTML.ElementFromString(content)
    ep_titles = html_elem.xpath('.//ul[@class="dramaSerialList"]//dt/span/text()')
    ep_summarys = []
    for item in html_elem.xpath('.//ul[@class="dramaSerialList"]//dd'):
        item_summary = '\n'.join(item.xpath('.//p/text()'))
        ep_summarys.append(item_summary)
    return ep_titles,ep_summarys


# DOWNLOAD TRAILER
def download_trail(url,extras_type,path1):
    html = HTTP.Request(url,headers=head,sleep=1.0)
    html_elem = HTML.ElementFromString(html)
    title = html_elem.xpath('//div[@id="content"]/h1/text()')[0].strip()    
    path = path1+"/"+title.replace('/','')+extras_type+".mp4"
    if os.path.exists(path) == 0 :
        mp4_url = html_elem.xpath('//video[@id]/source/@src')[0]   
        mp4 = HTTP.Request(mp4_url).content
        with io.open(path, 'wb+') as file:
            file.write(mp4)
        file.close()
       
def get_alltrail_link(trailpage_url,path1):
    html = HTTP.Request(trailpage_url)
    html_elem = HTML.ElementFromString(html)
    article = html_elem.xpath('//*[@class="mod"]')
    for page in article:
        key = page.xpath('.//h2/text()')[0]                     
        if key == "预告片 · · · · · ·":
            extras_type = "-trailer"
            num1 = trailer_num
        elif key == "片段 · · · · · ·":
            extras_type = "-short"
            num1 = short_num
        elif key == "花絮 · · · · · ·":
            extras_type = "-behindthescenes"
            num1 = behindthescenes_num
        else:
            extras_type = "-other"
            num1 = other_num
        if len(page.xpath('.//ul/li/a/@href')) <= num1 :
            num1 = len(page.xpath('.//ul/li/a/@href'))
        for i in  range(num1) :
            item = page.xpath('.//ul/li/a/@href')[i]
            download_trail(item,extras_type,path1)


#DOUBAN_TV_API
def douban_api_search_tv(results,media,lang):
    #Log(media.show)
    search_str = String.Quote(media.show)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        if os.path.exists(ip_path) is False:
            with io.open(ip_path, 'w+') as file:
              pass
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            if r == []:
              Log('写入初始内容')
              r=['1616401759.8','121.237.227.104:3000']
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(proxy)
        res = requests.get(DOUBAN_M_API_SEARCH % search_str,headers=headers,proxies=proxy)
        #Log(content.text())
        rt = json.loads(res.content)
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      rt = JSON.ObjectFromURL(DOUBAN_M_API_SEARCH % search_str,headers=headers,sleep=2.0)
    if len(rt)==0:
      pass
    else:
      for i, movie in enumerate(rt["subjects"]):
        try:
          if movie["type"] != "tv":
            continue
          score = 90
          movietitle = movie["title"]
          movieyear = movie["year"]
          #Log(movieyear)
          movieid = movie["id"]
          dist = String.LevenshteinDistance(movietitle.lower(), media.show.lower())
          dist = abs(dist)
          score = score - dist
          score = score - (5 * i)
          release_year = int(movieyear)
          media_year = None
          try:
                  media_year = int(media.year)
          except:
                  pass

          if media.year and media_year > 1900 and release_year:
                          year_diff = abs(media_year - release_year)
                          if year_diff <= 1:
                                          score = score + 10
                          else:
                                          score = score - (5 * year_diff)
          
          if score <= 0:
                  continue
          else:
                  results.Append(MetadataSearchResult(id=movieid, name=movietitle, year=movieyear, lang=lang, score=score))
        except:
          pass


def douban_api_update_tv(metadata,media,lang):
    id_str =String.Quote(metadata.id)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(metadata.id)
        res = requests.get(DOUBAN_M_API_TV % id_str,headers=headers,proxies=proxy)
        m = json.loads(res.content)
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      m = JSON.ObjectFromURL(DOUBAN_M_API_TV % id_str,headers=headers,sleep=1.0)
    #metadata.userRating = float(m['rating']['star_count']) * 2
    try:
      metadata.rating = float(m['rating']['value'])
      metadata.rating_image = 'rottentomatoes://image.rating.upright'
    except Exception as ex:
      Log(ex)  
    metadata.title = m['title']
    metadata.title_sort = pinyin(metadata.title)
    Log(metadata.title)
    metadata.summary = m['intro']
    #metadata.year = int(m['year'])
    #Log(metadata.year)
    metadata.original_title = m['original_title']
    try:
      metadata.originally_available_at = Datetime.ParseDate(m['pubdate'][0][0:10]).date()                 
    except:
      pass
    
    # Poster
    if len(metadata.posters.keys()) == 0:
            poster_url = m['pic']['large'].replace("m_ratio_poster", "l", 1)
            thumb_url = m['pic']['large'].replace("m_ratio_poster", "s", 1)
            metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)
            
  
    try:
      # Genres
      metadata.genres.clear()
      for genre in m['genres']:
          Log(genre)
          metadata.genres.add(genre)
    except:
      pass
    
    try:
    # Countries
      metadata.countries.clear()
      for country in m['countries']:
        metadata.countries.add(country.strip())

    except:
      pass

    # Roles
    try:
      if Prefs['ifproxy'] :
        res1 = requests.get(DOUBAN_M_API_TV_ROLES % id_str,headers=headers,proxies=proxy)
        r = json.loads(res1.content)
      else:
        r = JSON.ObjectFromURL(DOUBAN_M_API_TV_ROLES % id_str,headers=headers,sleep=1.0)
      metadata.roles.clear()
      for i, role in enumerate(r["actors"]):
        meta_role = metadata.roles.new()
        meta_role.name = role['name']
        meta_role.role = role['character']
        meta_role.photo = role['cover_url'].replace("s_ratio_celebrity", "l", 1)
        if i > 25 :
          break
    except:
      pass      

    # Reviews.
    try:
      if Prefs['ifproxy'] :
        res2 = requests.get(DOUBAN_M_API_TV_DUANPING % id_str,headers=headers,proxies=proxy)
        d = json.loads(res2.content)
      else:
        d = JSON.ObjectFromURL(DOUBAN_M_API_TV_DUANPING % id_str,headers=headers,sleep=1.0)
      metadata.reviews.clear()
      for i, review in enumerate(d["interests"]):
          r = metadata.reviews.new()
          r.author = review['user']['name']
          r.source = '豆瓣短评'
          r.image = 'rottentomatoes://image.review.fresh'
          r.link = review['sharing_url']
          r.text = review['comment']
    except:
      pass
    search_str = String.Unquote(metadata.title.replace(" ", ""))
    
    tv_url = search_baike(search_str,m['year'])
    ep_titles,ep_summarys = get_tvinfo(tv_url)
    #Log(type(ep_titles))
    #Log(ep_summarys)
    if ep_titles ==[]:
      tv_url = search_baike(search_str,'')
      #Log(tv_url)
      ep_titles,ep_summarys = get_tvinfo(tv_url)
      #Log(ep_titles)
    for s in media.seasons:
      # just like in the Local Media Agent, if we have a date-based season skip for now.
      for e in media.seasons[s].episodes:
        try:
          episode = metadata.seasons[s].episodes[e]
          episode.title = ep_titles[int(e)-1]
          episode.summary = ep_summarys[int(e)-1]
        except:
          pass
    #Trailer  
    if Prefs['ifdownloadtrailer'] :                         
        path = media.items[0].parts[0].file
        folder_path = os.path.dirname(path)                
        trailpage_url = DOUBAN_MOVIE_TRAILERURL % id_str
        get_alltrail_link(trailpage_url,folder_path)


#DOUBAN_MOVIE_API        
def douban_api_search(results,media,lang):
    #Log(ip_url)
    search_str = String.Quote(media.name)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        if os.path.exists(ip_path) is False:
            with io.open(ip_path, 'w+') as file:
              pass
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            if r == []:
              Log('写入初始内容')
              r=['1616401759.8','121.237.227.104:3000']
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(proxy)
        res = requests.get(DOUBAN_M_API_SEARCH % search_str,headers=headers,proxies=proxy)
        #Log(content.text())
        rt = json.loads(res.content)
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      rt = JSON.ObjectFromURL(DOUBAN_M_API_SEARCH % search_str,headers=headers,sleep=2.0)
    if len(rt)==0:
      pass
    else:
      for i, movie in enumerate(rt["subjects"]):
        try:
          if movie["type"] != "movie":
            continue
          score = 90
          movietitle = movie["title"]
          movieyear = movie["year"]
          #Log(movieyear)
          movieid = movie["id"]
          dist = String.LevenshteinDistance(movietitle.lower(), media.name.lower())
          dist = abs(dist)
          #dist_sub = String.LevenshteinDistance(movieorgtitle.lower(), media.name.lower())
          #dist_sub = abs(dist_sub)
          #if dist_sub<dist:
          #        dist = dist_sub
          score = score - dist

          score = score - (5 * i)
          release_year = int(movieyear)
          media_year = None
          try:
                  media_year = int(media.year)
          except:
                  pass

          if media.year and media_year > 1900 and release_year:
                          year_diff = abs(media_year - release_year)
                          if year_diff <= 1:
                                          score = score + 10
                          else:
                                          score = score - (5 * year_diff)
          
          if score <= 0:
                  continue
          else:
                  results.Append(MetadataSearchResult(id=movieid, name=movietitle, year=movieyear, lang=lang, score=score))
        except:
          pass

        
def douban_api_update(metadata,media,lang):
    id_str =String.Quote(metadata.id)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(metadata.id)
        res = requests.get(DOUBAN_M_API_MOVIE % id_str,headers=headers,proxies=proxy)
        m = json.loads(res.content)
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      m = JSON.ObjectFromURL(DOUBAN_M_API_MOVIE % id_str,headers=headers,sleep=1.0)
    #metadata.userRating = float(m['rating']['star_count']) * 2
    try:
      metadata.rating = float(m['rating']['value'])
      metadata.rating_image = 'rottentomatoes://image.rating.upright'
    except Exception as ex:
      Log(ex)  
    metadata.title = m['title']
    metadata.title_sort = pinyin(metadata.title)
    Log(metadata.title)
    metadata.summary = m['intro']
    metadata.year = int(m['year'])
    Log(metadata.year)
    metadata.original_title = m['original_title']
    try:
      metadata.originally_available_at = Datetime.ParseDate(m['pubdate'][0][0:10]).date()                 
    except:
      pass
    
    # Poster
    if len(metadata.posters.keys()) == 0:
            poster_url = m['pic']['large'].replace("m_ratio_poster", "l", 1)
            thumb_url = m['pic']['large'].replace("m_ratio_poster", "s", 1)
            metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)
            
    # Directors
    try:
      metadata.directors.clear()
      for director in m['directors']:
          meta_director = metadata.directors.new()
          meta_director.name = director['name']
    except:
      pass
    
    try:
      # Genres
      metadata.genres.clear()
      for genre in m['genres']:
          Log(genre)
          metadata.genres.add(genre)
    except:
      pass
    
    try:
    # Countries
      metadata.countries.clear()
      for country in m['countries']:
        metadata.countries.add(country.strip())

    except:
      pass

    
    # Roles
    try:
      if Prefs['ifproxy'] :
        res1 = requests.get(DOUBAN_M_API_ROLES % id_str,headers=headers,proxies=proxy)
        r = json.loads(res1.content)
      else:
        r = JSON.ObjectFromURL(DOUBAN_M_API_ROLES % id_str,headers=headers,sleep=1.0)
      metadata.roles.clear()
      for i, role in enumerate(r["actors"]):
        meta_role = metadata.roles.new()
        meta_role.name = role['name']
        meta_role.role = role['character']
        meta_role.photo = role['cover_url'].replace("s_ratio_celebrity", "l", 1)
        if i > 25 :
          break
    except:
      pass      

    # Reviews.
    try:
      if Prefs['ifproxy'] :
        res2 = requests.get(DOUBAN_M_API_DUANPING % id_str,headers=headers,proxies=proxy)
        d = json.loads(res2.content)
      else:
        d = JSON.ObjectFromURL(DOUBAN_M_API_DUANPING % id_str,headers=headers,sleep=1.0)
      metadata.reviews.clear()
      for i, review in enumerate(d["interests"]):
          r = metadata.reviews.new()
          r.author = review['user']['name']
          r.source = '豆瓣短评'
          r.image = 'rottentomatoes://image.review.fresh'
          r.link = review['sharing_url']
          r.text = review['comment']
    except:
      pass 
    #Trailer  
    if Prefs['ifdownloadtrailer'] :                         
        path = media.items[0].parts[0].file
        folder_path = os.path.dirname(path)                
        trailpage_url = DOUBAN_MOVIE_TRAILERURL % id_str
        get_alltrail_link(trailpage_url,folder_path)


#DOUBAN_MOVIE_XPATH
def douban_search(results,media,lang):
    search_str = String.Quote(media.name)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        if os.path.exists(ip_path) is False:
            with io.open(ip_path, 'w+') as file:
              pass
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            if r == []:
              Log('写入初始内容')
              r=['1616401759.8','121.237.227.104:3000']
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(proxy)
        content = requests.get(DOUBAN_MOVIE_SEARCH %search_str,headers=head,proxies=proxy).text
        Log(content)
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      content = HTTP.Request(DOUBAN_MOVIE_SEARCH %search_str,headers=head,sleep=1.0) 
    page = HTML.ElementFromString(content)
    x = page.xpath('//div[@class="result"]/div[2]/div/h3/a/text()')                 
    y = page.xpath('//div[@class="result"]/div[2]/div/div/span[@class="subject-cast"]/text()')          
    z = page.xpath('//div[@class="result"]/div[2]/div/h3/a/@onclick')             
    i = 0
    l = 10
    if len(x) <= 10:
        l = len(x)
    for i in range(l):
            score = 90
            movietitle = x[i]
            movieyear = y[i][-4:]
            movieid = get_str_btw(z[i], "sid: ", ", ")
            movieorgtitle = get_str_btw(y[i], "原名:", " /")
            dist = String.LevenshteinDistance(movietitle.lower(), media.name.lower())
            dist = abs(dist)
            dist_sub = String.LevenshteinDistance(movieorgtitle.lower(), media.name.lower())
            dist_sub = abs(dist_sub)
            if dist_sub<dist:
                    dist = dist_sub
            score = score - dist

            score = score - (5 * i)
            release_year = int(movieyear)
            media_year = None
            try:
                    media_year = int(media.year)
            except:
                    pass

            if media.year and media_year > 1900 and release_year:
                            year_diff = abs(media_year - release_year)
                            if year_diff <= 1:
                                            score = score + 10
                            else:
                                            score = score - (5 * year_diff)
            
            if score <= 0:
                    continue
            else:
                    results.Append(MetadataSearchResult(id=movieid, name=movietitle, year=movieyear, lang=lang, score=score))

def douban_update(metadata,media,lang):
    Log(metadata.id)
    #id_str =String.Quote(metadata.id.split('/')[0])
    id_str =String.Quote(metadata.id)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(metadata.id)
        content1 = requests.get(DOUBAN_MOVIE_SUBJECT % id_str,headers=head,proxies=proxy).text
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      content1 = HTTP.Request(DOUBAN_MOVIE_SUBJECT % id_str,headers=head,sleep=1.0)
    page1 = HTML.ElementFromString(content1)
    try:
      metadata.rating = float(page1.xpath('//*[@class="ll rating_num"]/text()')[0])
      metadata.rating_image = 'rottentomatoes://image.rating.upright'
      #metadata.rating_image = 'https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/certified_fresh.75211285dbb'
    except Exception as ex:
      Log(ex)  
    #Log(page1.xpath('//head/title/text()')[0].strip()[:-4])
    
    metadata.title = page1.xpath('//head/title/text()')[0].strip()[:-4]
    metadata.title_sort = pinyin(metadata.title)
    Log(metadata.title)
    #Log("".join(page1.xpath('//*[@property="v:summary"]/text()')).strip())
    metadata.summary = "".join(page1.xpath('//*[@property="v:summary"]/text()')).replace(" ", "").replace("\n", "")
    #Log(get_str_btw(page1.xpath('//*[@class="year"]/text()')[0], "(", ")"))
    metadata.year = int(get_str_btw(page1.xpath('//*[@class="year"]/text()')[0], "(", ")"))
    Log(metadata.year)
    #Log(page1.xpath('//*[@property="v:initialReleaseDate"]/text()')[0])
    metadata.original_title = page1.xpath('//*[@property="v:itemreviewed"]/text()')[0]
    try:
      metadata.originally_available_at = Datetime.ParseDate(page1.xpath('//*[@property="v:initialReleaseDate"]/text()')[0][0:10]).date()                 
    except:
      pass
    # Poster
    if len(metadata.posters.keys()) == 0:
            poster_url = page1.xpath('//*[@class="nbgnbg"]/img/@src')[0].replace("s_ratio_poster", "l", 1)
            thumb_url = page1.xpath('//*[@class="nbgnbg"]/img/@src')[0]
            metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)
    # Directors
    try:
      metadata.directors.clear()
      for director in page1.xpath('//*[@rel="v:directedBy"]/text()'):
              meta_director = metadata.directors.new()
              meta_director.name = director
    except:
      pass
    
    # Reviews.
    try:
      metadata.reviews.clear()
      for review in page1.xpath('//*[@id="hot-comments"]/div'):
          r = metadata.reviews.new()
          r.author = review.xpath('.//span[@class="comment-info"]/a/text()')[0]
          r.source = '豆瓣短评'
          r.image = 'rottentomatoes://image.review.fresh'
          r.link = review.xpath('.//span[@class="comment-info"]/a/@href')[0]
          if review.xpath('.//span[@class="full"]/text()'):
              r.text = "".join(review.xpath('.//span[@class="full"]/text()')).strip()
          else :
              r.text = "".join(review.xpath('.//span[@class="short"]/text()')).strip()
          #Log(r.text)
    except:
      pass
    try:
      # Genres
      metadata.genres.clear()
      for genre in page1.xpath('//*[@property="v:genre"]/text()'):
              Log(genre)
              metadata.genres.add(genre)
    except:
      pass    
    try:
    # Countries
      ii = 0
      ll = 20
      metadata.countries.clear()
      for ii in range(ll):
          if page1.xpath('//div[@id="info"]/*/text()')[ii] == "制片国家/地区:" :
              for country in page1.xpath('//div[@id="info"]/text()')[ii+1].split('/') :
                  metadata.countries.add(country.strip())
                  Log(country.strip())
          ii = ii + 1
    except:
      pass

    # Roles
    if Prefs['ifproxy'] :
        content = requests.get(DOUBAN_MOVIE_BASE % id_str,headers=head,proxies=proxy).text
    else:
        content = HTTP.Request(DOUBAN_MOVIE_BASE % id_str,headers=head,sleep=1.0)
    page = HTML.ElementFromString(content)
    y = page.xpath('//*[@class="info"]/span[1]/a/text()')  
    z = page.xpath('//*[@class="info"]/span[2]/text()')         
    x = page.xpath('//*[@class="celebrity"]/a/div/@style') 
    l = 20
    i=1      
    
    if len(y) <= 20:               
        l = len(y)
    metadata.roles.clear()
    for i in range(l):
            meta_role = metadata.roles.new()
            meta_role.name = y[i].split(" ")[0]
            meta_role.role =get_str_btw(z[i], " (", ")")
            meta_role.photo = get_str_btw(x[i], "url(", ")")
    
    try:
      m = JSON.ObjectFromString(page1.xpath('//*[@type="application/ld+json"]/text()')[0])
      #Log(m)
      # Writers
      metadata.writers.clear()
      for writer in m["author"]:
              Log(writer["name"])
              meta_writer = metadata.writers.new()
              meta_writer.name = writer["name"].split(" ")[0]
    except:
      pass
    #Trailer
  
    if Prefs['ifdownloadtrailer'] :                         
        path = media.items[0].parts[0].file
        folder_path = os.path.dirname(path)                
        trailpage_url = DOUBAN_MOVIE_TRAILERURL % id_str
        get_alltrail_link(trailpage_url,folder_path)


#DOUBAN_TV_XPATH
def douban_search_tv(results,media,lang):
    search_str = String.Quote(media.show)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        if os.path.exists(ip_path) is False:
            with io.open(ip_path, 'w+') as file:
              pass
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            if r == []:
              Log('写入初始内容')
              r=['1616401759.8','121.237.227.104:3000']
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(proxy)
        content = requests.get(DOUBAN_MOVIE_SEARCH %search_str,headers=head,proxies=proxy).text
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      content = HTTP.Request(DOUBAN_MOVIE_SEARCH %search_str,headers=head,sleep=1.0)
    page = HTML.ElementFromString(content)
    x = page.xpath('//div[@class="result"]/div[2]/div/h3/a/text()')                 
    y = page.xpath('//div[@class="result"]/div[2]/div/div/span[@class="subject-cast"]/text()')           
    z = page.xpath('//div[@class="result"]/div[2]/div/h3/a/@onclick')              
    i = 0
    l = 10
    if len(x) <= 10:
        l = len(x)
    for i in range(l):
            score = 90
            movietitle = x[i]
            movieyear = y[i][-4:]
            movieid = get_str_btw(z[i], "sid: ", ", ")
            movieorgtitle = get_str_btw(y[i], "原名:", " /")
            dist = String.LevenshteinDistance(movietitle.lower(), media.show.lower())
            dist = abs(dist)
            dist_sub = String.LevenshteinDistance(movieorgtitle.lower(), media.show.lower())
            dist_sub = abs(dist_sub)
            if dist_sub<dist:
                    dist = dist_sub
            score = score - dist

            score = score - (5 * i)
            release_year = int(movieyear)
            media_year = None
            try:
                    media_year = int(media.year)
            except:
                    pass

            if media.year and media_year > 1900 and release_year:
                            year_diff = abs(media_year - release_year)
                            if year_diff <= 1:
                                            score = score + 10
                            else:
                                            score = score - (5 * year_diff)
                                            
            if score <= 0:
                    continue
            else:
                    # All parameters MUST be filled in order for Plex find these result.
                    results.Append(MetadataSearchResult(id=movieid, name=movietitle, year=movieyear, lang=lang, score=score))


def douban_update_tv(metadata,media,lang):
    Log('开始更新')
    id_str =String.Quote(metadata.id)
    if Prefs['ifproxy'] :
      try:
        ticks = time.time()
        with io.open(ip_path, 'r+') as file:
            r = file.readlines()
            old_ticks = float(r[0])
            ip = r[1]
            timestamp = ticks - old_ticks
            if timestamp > 30 :
              new_ip = HTTP.Request(ip_url,headers=hea,sleep=1.0).content
              ip = unicode(new_ip)
              file.seek(0)
              file.truncate() 
              file.write(unicode(str(ticks),'utf-8') + "\n")
              file.write(ip)
        proxy = {'http':ip,'https':ip}
        Log(metadata.id)
        content1 = requests.get(DOUBAN_MOVIE_SUBJECT % id_str,headers=head,proxies=proxy).text
      except Exception as ex:
        Log("代理错误")
        Log(ex) 
    else:
      content1 = HTTP.Request(DOUBAN_MOVIE_SUBJECT % id_str,headers=head,sleep=1.0)
    page1 = HTML.ElementFromString(content1)
    try:
      metadata.rating = float(page1.xpath('//*[@class="ll rating_num"]/text()')[0])
      metadata.rating_image = 'rottentomatoes://image.rating.upright'
    except:
      pass   
    #Log(page1.xpath('//head/title/text()')[0].strip()[:-4])
    metadata.title = page1.xpath('//head/title/text()')[0].strip()[:-4]
    metadata.title_sort = pinyin(metadata.title)
    #Log("".join(page1.xpath('//*[@property="v:summary"]/text()')).strip())
    metadata.summary = "".join(page1.xpath('//*[@property="v:summary"]/text()')).strip()
    #Log(get_str_btw(page1.xpath('//*[@class="year"]/text()')[0], "(", ")"))
    year = get_str_btw(page1.xpath('//*[@class="year"]/text()')[0], "(", ")")
    Log(page1.xpath('//*[@property="v:itemreviewed"]/text()')[0])
    metadata.original_title = page1.xpath('//*[@property="v:itemreviewed"]/text()')[0]
    Log(metadata.original_title)
    try:
      metadata.originally_available_at = Datetime.ParseDate(page1.xpath('//*[@property="v:initialReleaseDate"]/text()')[0][0:10]).date()                 
    except:
      pass
    
    # Poster
    if len(metadata.posters.keys()) == 0:
            poster_url = page1.xpath('//*[@class="nbgnbg"]/img/@src')[0].replace("s_ratio_poster", "l", 1)
            thumb_url = page1.xpath('//*[@class="nbgnbg"]/img/@src')[0]
            metadata.posters[poster_url] = Proxy.Preview(HTTP.Request(thumb_url), sort_order=1)

    try:
    # Countries
      ii = 0
      ll = 20
      metadata.countries.clear()
      for ii in range(ll):
          if page1.xpath('//div[@id="info"]/*/text()')[ii] == "制片国家/地区:" :
              for country in page1.xpath('//div[@id="info"]/text()')[ii+1].split('/') :
                  metadata.countries.add(country.strip())
                  Log(country.strip())
          ii = ii + 1
    except:
      pass
    #Log(page1.xpath('//*[@type="application/ld+json"]/text()')[0])
    try:
      # Genres
      metadata.genres.clear()
      for genre in page1.xpath('//*[@property="v:genre"]/text()'):
              Log(genre)
              metadata.genres.add(genre)
    except:
      pass    
     # Roles
    id_str =String.Quote(metadata.id)
    if Prefs['ifproxy'] :
        content = requests.get(DOUBAN_MOVIE_BASE % id_str,headers=head,proxies=proxy).text
    else:
        content = HTTP.Request(DOUBAN_MOVIE_BASE % id_str,headers=head,sleep=1.0)
    page = HTML.ElementFromString(content)
    y = page.xpath('//*[@class="info"]/span[1]/a/text()')   
    z = page.xpath('//*[@class="info"]/span[2]/text()')        
    x = page.xpath('//*[@class="celebrity"]/a/div/@style') 
    l = 20
    i=1      
    
    if len(y) <= 20:               
        l = len(y)
    metadata.roles.clear()
    for i in range(l):
            meta_role = metadata.roles.new()
            meta_role.name = y[i].split(" ")[0]
            meta_role.role =get_str_btw(z[i], " (", ")")
            meta_role.photo = get_str_btw(x[i], "url(", ")")


    search_str = String.Unquote(metadata.title.replace(" ", ""))
    tv_url = search_baike(search_str,year)
    ep_titles,ep_summarys = get_tvinfo(tv_url)
    #Log(type(ep_titles))
    #Log(ep_summarys)
    if ep_titles ==[]:
      tv_url = search_baike(search_str,'')
      #Log(tv_url)
      ep_titles,ep_summarys = get_tvinfo(tv_url)
      #Log(ep_titles)
    for s in media.seasons:
      # just like in the Local Media Agent, if we have a date-based season skip for now.
      for e in media.seasons[s].episodes:
        try:
          episode = metadata.seasons[s].episodes[e]
          episode.title = ep_titles[int(e)-1]
          episode.summary = ep_summarys[int(e)-1]
        except:
          pass

              
class DoubanAgent(Agent.Movies):
	name = 'Douban'
	languages = [Locale.Language.Chinese]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia',
                        'com.plexapp.agents.zimuku',
                        'com.plexapp.agents.opensubtitles']
	contributes_to = ['com.plexapp.agents.imdb']

	def search(self, results, media, lang):
            if Prefs['agent_select'] == "douban" :
                douban_search(results,media,lang)
            if Prefs['agent_select'] == "doubanapi" :
                douban_api_search(results,media,lang)
		

	def update(self, metadata, media, lang):
            if Prefs['agent_select'] == "douban" :
		douban_update(metadata,media,lang)
            if Prefs['agent_select'] == "doubanapi" :
                douban_api_update(metadata,media,lang)
                
class Douban(Agent.TV_Shows):
	name = 'Douban'
	languages = [Locale.Language.Chinese, Locale.Language.English]
	primary_provider = True
	accepts_from = ['com.plexapp.agents.localmedia']
	contributes_to = ['com.plexapp.agents.thetvdb']

	def search(self, results, media, lang):
            if Prefs['tv_agent_select'] == "douban" :
		douban_search_tv(results,media,lang)
            if Prefs['tv_agent_select'] == "doubanapi" :
                douban_api_search_tv(results,media,lang)
	def update(self, metadata, media, lang):
            if Prefs['tv_agent_select'] == "douban" :
		douban_update_tv(metadata,media,lang)
            if Prefs['tv_agent_select'] == "doubanapi" :
		douban_api_update_tv(metadata,media,lang)

class Douban(Agent.Photos):
  name = 'Douban'
  primary_provider = True
  # Expose some languages for Photo sections to use with the Imagga API.
  languages = [Locale.Language.Chinese, Locale.Language.English]
  contributes_to = ['com.plexapp.agents.none']

  def search(self, results, media, lang):
    Log('我在这里')
    results.Append(MetadataSearchResult(id=media.id, name=media.title, year=None, lang=lang, score=100))

  def update(self, metadata, media, lang):
    Log('我在这里2')
    metadata.title = media.title
    genre = '测试标签'
    metadata.tags.add(genre)
    Log(metadata.tags)
    
              
			
# -- LOG ADAPTER -------------------------------------------------------------

class PlexLogAdapter(object):
    """
    Adapts Plex Log class to standard python logging style.

    This is a very simple remap of methods and does not provide
    full python standard logging functionality.
    """
    debug = Log.Debug
    info = Log.Info
    warn = Log.Warn
    error = Log.Error
    critical = Log.Critical
    exception = Log.Exception


class doubanLogAdapter(PlexLogAdapter):
    """
    Plex Log adapter that only emits debug statements based on preferences.
    """
    @staticmethod
    def debug(*args, **kwargs):
        """
        Selective logging of debug message based on preference.
        """
        Log.Debug(*args, **kwargs)

log = doubanLogAdapter
