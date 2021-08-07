# 前置声明
此项目为[2Dou/watermarker](https://github.com/2Dou/watermarker)大佬的项目派生
本项目主要用于hexo+github图床批量添加水印
经过本人测试发现原项目在对gif图片添加水印时会导致gif动图无法使用，特做此派生解决此问题
顺便修复原项目几个bug，添加了几个关键参数的注释，方便直接在代码里修改参数

![](https://cdn.jsdelivr.net/gh/QiYi92/ImageHost/img/202108080037002.png)

# 执行
将需要上水印的图片扔在img文件夹即可
```
python marker.py -f ./img -m 添加水印
```
如果需要修改输出文件夹，直接在源码中修改-o参数的default的值即可
# marker.py

为图片添加文字水印
可设置文字**大小、颜色、旋转、间隔、透明度**

# usage

需要 PIL 库 `pip install Pillow`

```
usage: marker.py [-h] [-f FILE] [-m MARK] [-o OUT] [-c COLOR] [-s SPACE]
                 [-a ANGEL] [--size SIZE] [--opacity OPACITY]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  image file path or directory
  -m MARK, --mark MARK  watermark content
  -o OUT, --out OUT     image output directory, default is ./output
  -c COLOR, --color COLOR
                        text color like '#000000', default is #8B8B1B
  -s SPACE, --space SPACE
                        space between watermarks, default is 75
  -a ANGEL, --angel ANGEL
                        rotate angel of watermarks, default is 30
  --size SIZE           font size of text, default is 50
  --opacity OPACITY     opacity of watermarks, default is 0.15
  --quality QUALITY     quality of output images, default is 90
```

# 效果

`python marker.py -f ./input/test.png -m 添加水印`

![](https://github.com/2Dou/watermarker/raw/master/output/test.png)
