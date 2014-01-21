import SocketServer
import webbrowser
import urllib2
import os
'''

    Copyright (C) Ulvi Ibrahimov Winter 2014 CMPUT 410 University of Alberta

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 '''

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        fileName=""
        self.data = self.request.recv(1024).strip()
        if self.data != "":
            userData=self.data.split()
            fileName=self.handlePath(userData[1])
        if(fileName=="www/"):
            fileName="www/index.html"
        elif fileName=="www/deep":
            fileName="www/deep/index.html"
        try:
            testF=open(fileName,"r")
            testF.close()
        except :
            self.request.sendall("HTTP/1.1 404 Not Found\n")
        if "deep/index.html" in fileName:
            self.displayIndex("www/deep/index.html")       
        elif "deep.css" in fileName:       
            self.displayCss("www/deep/deep.css")        
        elif "etc/group" in fileName:
            self.request.sendall("HTTP/1.1 404 Not Found\n")
        elif "index.html" in fileName:
            self.displayIndex("www/index.html")
        elif "base.css" in fileName:
            self.displayCss("www/base.css")
        
                          
    def displayIndex(self,indexType):
        header="HTTP/1.1 200 OK\nContent-type: text/html\r\n\r\n"
        f = open(indexType, 'r')
        dataToSend=header
        for line in f:
            dataToSend=dataToSend+line
        f.close()
        self.request.sendall(dataToSend)
    def displayCss(self,CssType):
        header="HTTP/1.1 200 OK\nContent-type: text/css\r\n\r\n"
        f = open(CssType, 'r')
        dataToSend=header
        for line in f:
            dataToSend=dataToSend+line
        f.close()
        self.request.sendall(dataToSend)

    def handlePath(self, userPath):
        if(userPath[0]=="/"):
            newUserPath=userPath[1:len(userPath)]
        if(userPath[len(userPath)-1]=="/"):
            newUserPath=newUserPath[0:len(newUserPath)-1]
        newUserPath="www/"+newUserPath
        return newUserPath
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
    server.serve_forever()
