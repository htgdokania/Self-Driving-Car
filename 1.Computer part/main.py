import numpy as np
import cv2
import socket
import send_data_pi 

class VideoStreaming(object):
    
    def __init__(self, host, port):        
        self.server_socket = socket.socket()
        self.server_socket.bind(('', port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()
                
    def streaming(self):
        try:
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    lane_image=np.copy(image)
                    lane_image,red=self.checkforred(lane_image)
                    if red:
                        self.sendinfoback(0,0,1)
                    else:
                        canny=self.canny(lane_image)
                        roi=self.region_of_interest(canny)
                        lane=cv2.bitwise_and(canny,roi)
                        lines=cv2.HoughLinesP(lane,1,np.pi/180,30,np.array([]),minLineLength=20,maxLineGap=5)                    
                        self.average_slope_intercept(lines,lane_image) 
                        line_image=self.display_lines(lines,lane_image)                    
                        lane_image=cv2.addWeighted(lane_image,1,line_image,1,0)

                    cv2.imshow('canny',canny)
                    cv2.imshow('roi',roi)
                    cv2.imshow('lane',lane)
                    cv2.imshow('line',line_image)
                    cv2.imshow('frame',lane_image) #display image    
                    key=cv2.waitKey(1) & 0xFF
                    if  key == ord('q'):
                        send_data_pi.Tcp_Close()
                        break        
        finally:
            self.connection.close()
            self.server_socket.close()

    def sendinfoback(self,l,r,red):
        D=b''
        D+=bytes([l,r,red])
        print('here inside sendinfo',D)
        send_data_pi.Tcp_Write(D)
        
    def checkforred(self,image):
        font = cv2.FONT_HERSHEY_SIMPLEX
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        #Red HSV Range
        low_red=np.array([157,56,0])
        high_red=np.array([179,255,255])
        
        mask=cv2.inRange(hsv,low_red,high_red)
        blur=cv2.GaussianBlur(mask,(15,15),0)
        contours,_=cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        status=0
        for contour in contours:
            area=cv2.contourArea(contour)
            if area>20000:
                status=1
                cv2.drawContours(image,contour,-1,(0,0,255),3)
                cv2.putText(image,'RED STOP',(240,320), font, 2,(0,0,255),2,cv2.LINE_AA)     
        return (image,status)

    def average_slope_intercept(self,lines,image):
        left_fit=[]
        right_fit=[]
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2=line.reshape(4)
                parameters=np.polyfit((x1,x2),(y1,y2),1)
                slope=parameters[0]
                intercept=parameters[1]
                if slope<0:
                    right_fit.append((slope,intercept))
                else:
                    left_fit.append((slope,intercept))
                    
        left_fitavg=np.average(left_fit, axis=0)
        right_fitavg=np.average(right_fit, axis=0)
        print("left slope",left_fitavg,"rigt slope",right_fitavg)
        self.sendinfoback(len(left_fit), len(right_fit),red=0) # Send number of left and right lines detected.

    def canny(self,image):
        gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        blur=cv2.GaussianBlur(gray, (7,7), 0)
        canny=cv2.Canny(blur,50,150)  # lowerThreshold=50 UpperThreshold=150 
        return canny

    def region_of_interest(self,image):
        height=image.shape[0]
        width=image.shape[1]
        region=np.array([[(100,height),(width-100,height),(width-100,height-120),(100,height-120)]])
        mask=np.zeros_like(image)
        cv2.fillPoly(mask,region, 255)
        return mask
    
    def display_lines(self,lines,image):
        line_image=np.zeros_like(image)
        if lines is not None:
            for line in lines:
                if len(line)>0:                    
                    x1,y1,x2,y2=line.reshape(4)
                    cv2.line(line_image,(x1,y1),(x2,y2),[0,255,0],10)
        return line_image

if __name__ == '__main__':
    # host, port
    h, p = "", 8000
    VideoStreaming(h, p)

cv2.destroyAllWindows()