from urllib        import urlopen
from BeautifulSoup import BeautifulSoup
from random        import choice
from re            import sub
from sqlite3       import connect
from time          import sleep
from threading     import Thread

def pdrink( lnk ):
  ## parse drink from html

  def lncn( ln ):
     ln   = str( ln.split('">')[-1] )
     ln  = str( ln.split('<')[0] )
     return ln

  def pgrents( seg ):
     grt = []
     qua = []
     ret = []
     seg = str( sub( '\\n', '', seg ) )
     seg = str( sub( '  ', '', seg ) )

     for ln in seg.split('<tr>'):
       ln = str( ln ).strip()

       if '</td><td>' in ln:
          qty = str( ln.split('</td><td>')[0] )
          qty = str( qty.split('>')[-1] )
          ing = str( ln.split('</td><td>')[-1] )

          if 'href' in ing:
            ing = lncn( ing ).strip()

          else:
            ing = str( ing.split('<td>')[-1] )
            ing = str( ing.split('<')[0] ).strip()

          c = { qty: ing }
          ret.append( c )

     return ret

  def dsc( html ):

     for ln in html.split('\n'):
       ln = str( ln )

       if '<br>' in ln:
          if '</td>' in ln:

            ln = str( ln.split('<br>')[-1] )
            ln = str( ln.split('<')[0] )

            return ln

  def addent( tl, cat, gladd, ingre,  inst ):

     con = connect('bar.db')
     with con:
       cur = con.cursor()
       #cur.execute( "DROP TABLE IF EXISTS Drinks" )
       try:
          cur.execute( "CREATE TABLE Drinks (Name TEXT, Category TEXT, Glass TEXT, Ingredients TEXT, Instructions TEXT )" )
       except:
          pass

       cur.execute( "INSERT INTO Drinks VALUES(?,?,?,?,?)", [(tl),(cat),(glass),(ingre),(inst)] )

     con.close()


  proxies = {'http': 'http://127.0.0.1:3128'}
  rsp     = urlopen( lnk, proxies=proxies )
  #info    = rsp.info()
  html    = rsp.read()
  hl      = str( html )
  rsp.close()

  soup    = BeautifulSoup( html )
  tl      = str( soup.find('span', attrs={'class': 'title_text '}) ).split(': ')[-1]
  tl      = str( tl.split('<')[0] )
  tl      = str( sub( '&amp;', 'n', tl ) )
  tl      = str( sub( '#', '', tl ) )

  glc     = soup.findAll('td', attrs={'valign': 'top', 'nowrap': 'nowrap'})

  glc1    = str( glc[1] )
  glc2    = str( glc[2] )

  cat     = str( lncn( glc1 ) )
  glass   = str( lncn( glc2 ) )

  seg     = str( hl.split('cellpadding="2"')[-1] )
  seg     = str( seg.split('table')[0])
  ingre   = str( pgrents( seg ) )
  inst    = str( dsc( html ) )

  #data    = [(tl),(cat),(glass),(ingre),(inst)]
  addent( tl, cat, glass, ingre, inst )


def readbar():

  con = connect('bar.db')
  with con:
     cur = con.cursor()


     cur.execute( "SELECT * FROM Drinks" )

     rows = cur.fetchall()
     for row in rows:
       print row

  con.close()


def dadada():
  lnks = []
  proxies = {'http': 'http://127.0.0.1:3128'}
  rsp  = urlopen('http://www.barmeister.com/drinks/top100', proxies=proxies )
  info = rsp.info()
  #print( info )

  html = rsp.read()
  rsp.close()

  soup = BeautifulSoup( html )
  href = soup.findAll('a')

  for a in href:
     a = str( a )
     l = str( a.split('="')[-1] )
     l = str( l.split('"')[0] )

     if 'top' in l:
        if 'recipe' in l:
          l = str( 'http://www.barmeister.com%s' % l )
          lnks.append( l )

  #l = choice( lnks )
  for l in lnks:
     l = str( l )
     l = u'%s' % l
     print( 'fetching %s' % l )
#     t = Thread( target=pdrink, args=( str(l) )  )
#     t.start()
     r = pdrink( l )
#     sleep( 5 )

  readbar()

if __name__ == "__main__":
  dadada()

