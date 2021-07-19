class GlobalVar():
    def __init__(self,global_frame=0,is_begin=False,video_choice=0):
        self.global_frame1=global_frame
        self.global_frame2=global_frame
        self.global_frame3=global_frame
        self.global_frame4=global_frame
        self.global_frame5=global_frame
        self.is_begin=is_begin
        self.video_choice=video_choice
        self.collect=False
    def get_global_frame1(self):
        return self.global_frame1
    def set_global_frame1(self,frame):
        self.global_frame1=frame
    def get_global_frame2(self):
        return self.global_frame2
    def set_global_frame2(self,frame):
        self.global_frame2=frame
    def get_global_frame3(self):
        return self.global_frame3
    def set_global_frame3(self,frame):
        self.global_frame3=frame
    def get_global_frame4(self):
        return self.global_frame4
    def set_global_frame4(self,frame):
        self.global_frame4=frame
    def get_global_frame5(self):
        return self.global_frame5
    def set_global_frame5(self,frame):     #采集人脸的帧数据
        self.global_frame5=frame
    def set_collect(self,collect):
        self.collect=collect
    def get_collect(self):
        return self.collect
    def get_is_begin(self):
        return self.is_begin
    def set_is_begin(self,begin):
        self.is_begin=begin
    def set_video_choice(self,video_choice):
        self.video_choice=video_choice
    def get_video_choice(self):
        return self.video_choice

globalvar=GlobalVar()