#!/usr/bin/env python3

from sqlite3 import connect
from re import sub

def csso( maxl ):
  src = str( '''\

#f2_container {
  position: relative;
  width: 460px; height: %s;
  right: 0; left: 0; top: 66px;
  margin-top 1.5s ease-in-out;
  margin-bottom 1.5s ease-in-out;
  top 1.5s ease-in-out;
  bottom 1.5s ease-in-out;
}

#f1_container {
  position: relative;
  margin: 10px auto;
  width: 450px;
  height: 280px;
  margin-top 1.5s ease-in-out;
  z-index: 1;
}

#f1_container {
  perspective: 1000;
  transition-timing-function: ease-in;
  transition: 0.5s;
  margin-top 1.5s ease-in-out;
}

#f1_card {
  width: 450px;
  height: 280px;
  transform-style: preserve-3d;
  transition: all 1.0s linear;
  margin-top 0.5s ease-in-out;
}

#f1_container:hover #f1_card {
  transform: rotateY(180deg);
  box-shadow: -5px 5px 5px #aaa;
}

.face {
  position: absolute;
  z-index: 5;
  width: 100%%;
  height: 100%%;
  backface-visibility: hidden;
}
.face.front{
  background-color: #aaa;
}

.face.back {
  transform: rotateY(180deg);
  box-sizing: border-box;
  padding: 10px;
  color: white;
  text-align: center;
  background-color: #aaa;
}

div#header-wrapper {
    z-index:10;
    background-color: #00FF00;
    font-color:yellow;
    width:100%%;       top:0;
    left:0;           right:0;
    position: absolute;
    height:66px;
}

body>div#header-wrapper {
    position:relative;
    margin:0 auto;
    top:0; left:0;
    right:0;
}

div#header {
    height:66px;
    position: fixed;
    left:0; right:0;
    font-color: yellow;
    margin:0 auto;
    background-color: #00FF00;
    color: #00FF00;
    font-style: oblique;
    font-size: 36px;
    top: 0;
    text-align: center;
    left: 15; right: 15;
}


.cfont{ font-size: 20px; }

.c-l{ float: left; width: 45%%; }
.c-r{ float: right; width: 45%%; }

.column-left{ float: left; width: 33%%; left:50px; bottom: 0; }
.column-right{ float: right; width: 33%%; right:50px; bottom: 0; }
.column-center{ display: inline-block; width: 33%%; }

''' % maxl )
  return src

def magiks():
  ### assert element position from button selection
  src = '''\
  function pswitch( ptr ) {

    var element = document.getElementById( 'f2_container' ),
    style       = window.getComputedStyle( element ),
    top         = style.getPropertyValue( 'top' );
    top         = +top.replace('px','');

    if ( top == 66 ) {
       if ( ptr == "down" ) {
         return;
       }
    }

    if ( ptr == "up" ) {
      top = top - 290;
    } else {
      top = top + 290;
    }

    top               = top + 'px';
    console.log( ptr,top );
    element.style.top = top;
  }

  '''
  return src

def tails():
  src = '''\
  </div>
    <div id="header-wrapper"><div id="header"><pre>
    <button id="up" value="UP" onclick="pswitch('up');">DOWN</button><button id="down" value="DOWN" onclick="pswitch('down');">UP</button></pre>
  </pre></div></div>
  </body></html>'''
  return src


def clnln( ln ):
  ln = str( ln )

  ln = str( sub( '\[', '', ln ) )
  ln = str( sub( '\{', '', ln ) )
  ln = str( sub( '\]', '', ln ) )
  ln = str( sub( '\}', '', ln ) )
  ln = str( sub( "'", "", ln ) )
  ln = str( sub( '"', '', ln ) )

  return ln


def readbar():

  m = str( magiks() )
  t = str( tails() )
  con = connect('bar.db')
  with con:
     cur = con.cursor()
     cur.execute( "SELECT * FROM Drinks" )

     rows = cur.fetchall()

     ### average legth * total cards = max length
     al   = 290
     lr   = len( rows )
     maxl = int( lr * al )

     cs   = str( csso( maxl ) )
     htm  = str( '<hmtl><head><style>\n\n%s\n\n</style><script>\n\n%s\n\n</script></head><body><div id="f2_container">' % ( cs, m ) )
     print( htm )

     #print( 'max length %d' % maxl )

     for row in rows:
       tl  = row[0]
       cat = row[1]
       gls = row[2]
       ing = row[3]
       ins = row[4]
       igz = '<div class="c-l">'
       n   = 0
       p   = []

       for r in ing.split("}, {"):
         r = str( r )

         q = str( r.split(': ')[0] )
         q = str( clnln( q ) )
         i = str( r.split(': ')[-1] )
         i = str( clnln( i ) )

         z = [ q, i ]
         p.append( z )
         #igz = str( '%s\n%s %s<br>' % ( igz, q, i ) )

       lq = len( p )
       hq = int( round( float(lq)/float(2) ) )
       for h, g in p:
           if n == hq:
             igz = str( '%s\n\n</div><div class="c-r">\n' % igz )

           h   = str( h )
           g   = str( g )
           igz = str( '%s\n%s %s<br>' % ( igz, h, g ) )

           if n == lq:
              igz = str( '%s\n</div>' % igz )
              break

           n   = n + 1

       igz = str( '%s\n</div><br><br><br>\n\n' % igz )
       sec = str( '''\
  <div id="f1_container">
  <div id="f1_card" class="shadow">
    <div class="front face"><div class="cfont">
      <center><bold><u><pre>%s</pre></u></bold></center>
    </div></div>
    <div class="back face center">
      <pre> %s </pre>
       Category:  %s &emsp;-&emsp; Glass:  %s<br>
      <p>%s</p>
      <textarea style="width:365px; height: 75px; resize:none;">%s</textarea>
      <div class="column-left">
       <button id="up" value="UP" onclick="pswitch('up');">DOWN</button></div>
      <div class="column-right">
     <button id="down" value="DOWN" onclick="pswitch('down');">UP</button>
    </div></div>
  </div></div>

''' % ( tl, tl, cat, gls, igz, ins  ) )
       print(sec)

  con.close()
  print( t  )

if __name__=="__main__":
  readbar()
