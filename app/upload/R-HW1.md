## 计算机图形学作业一

#### 姓名：陈俊帆    学号：22336033

### 环境搭建

#### 配置IDE

在官网下载Visual Studio 2022并正常运行安装即可

#### 配置Qt

根据教程打开下载地址`http://download.qt.io/official_releases/qt/5.13/5.13.0/ `，发现页面已不存在

![alt text](image.png)

然后进入前项下载页面，选择新版本`6.8.0`，并不存在教程中的`exe`文件下载

![alt text](image-1.png)

在网上查询新的教程，进入QT官方网站`https://www.qt.io/zh-cn/`

![alt text](image-2.png)

注册账号并下载`qt-online-installer-windows-x64-4.8.1`，在注册账号过程中因为验证码发到手机过程时间较长，需要耐心等待短信并且及时进行邮箱认证，否则会出现后续安装前登录账号认证不成功的情况

下载完成后打开安装程序，用在网页上注册好的账号登录即可

![alt text](image-3.png)

（因为邮箱认证失败，此处我重新跳过网页中免费试用的认证，直接简单注册一个新的账号并且进行邮箱认证，最终成功进行安装）

然后指定安装目录，勾选`QT 6.8.0`以及其他组件，等待安装完成即可，该过程大约需要一小时

#### 安装Qt VS Tools拓展并配置

根据配置环境教程，启动VS2022并跳过登录过程，在拓展栏中搜索`Qt`，可以找到`Qt Visual Studio Tools`，点击安装拓展（此处是完成后的截图）

![alt text](image-4.png)

等待较长时间拓展仍未开始安装，进行翻墙也安装失败，可能是网络代理问题，重新查询相关解决方案，进入官方下载地址`https://download.qt.io/development_releases/vsaddin/`

![alt text](image-5.png)

下载完成进行安装，安装完成后重启VS2022，此时再打开菜单栏的`拓展`选项，已经存在`Qt VS Tools`

![alt text](image-6.png)

进入`Options`进行配置，点击`Qt->Versions->Add`，选择`Qt 6.8.0`的安装目录，点击`Add`，然后点击`OK`完成配置，此处已经设置为`Default`，无需手动调整

![alt text](image-7.png)

#### 环境配置

根据实验教程，将`D:qt\6.8.0\msvc2022_64\bin`添加到环境变量中，在Demo文件夹中打开终端并执行`qmake -tp vc`，报错`Cannot run compiler 'cl'，再将`D:\VS\visual studio\VC\Tools\MSVC\14.41.34120\bin\Hostx64\x64`加入环境变量即可

![alt text](image-8.png)

此时重新打开cmd并执行`qmake -tp vc`，成功生成`CGTemplate.vcxproj`等文件

![alt text](image-9.png)

#### Demo运行

用VS打开`CGTemplate.vcxproj`文件，运行`main.cpp`，报错缺失`GL/glew.h`

![alt text](image-10.png)

查询资料得知需要手动配置`glew`库，进入`http://glew.sourceforge.net/`并下载`glew-2.1.0.win32.zip`，解压并将其`include`路径加入`CGTemplate.pro`中

![alt text](image-11.png)

终端中执行`qmake -tp vc`重新生成项目，再次尝试用VS打开并运行`main.cpp`，此时报错不存在`QOpenGLWidget`引用，打开`Qt`文件夹中`msvc2022_64/include`目录，发现`QtOpenGLWidget`在`QtWidgets`中，因此需要将`QtWidgets`加入`CGTemplate.pro`

![alt text](image-12.png)

修改后的`CGTemplate.pro`代码段如下：

![alt text](image-13.png)

再次重新在终端中执行`qmake -tp vc`，用VS打开并运行`main.cpp`，报错`glew32.lib`缺失，查询资料得知，可以右键`CGTemplate`打开`属性->配置属性->链接器->附加库目录`加入路径`D:\glew-2.1.0\lib\Release\x64`，再次打开终端执行`qmake -tp vc`重新生成文件，此时成功运行`main.cpp`，出现窗口

![alt text](img/test.png)

### 绘制平面姓名首字母

#### 代码实现

具体的`myglwidget.cpp`代码实现如下：

```
#include "myglwidget.h"

MyGLWidget::MyGLWidget(QWidget *parent)
	:QOpenGLWidget(parent),
	scene_id(0)
{
}

MyGLWidget::~MyGLWidget()
{

}

void MyGLWidget::initializeGL()
{
	glViewport(0, 0, width(), height());
	glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
	glDisable(GL_DEPTH_TEST);
}

void MyGLWidget::paintGL()
{
	if (scene_id==0) {
		scene_0();
	}
	else {
		scene_1();
	}
}

void MyGLWidget::resizeGL(int width, int height)
{
	glViewport(0, 0, width, height);
	update();
}

void MyGLWidget::keyPressEvent(QKeyEvent *e) {
	//Press 0 or 1 to switch the scene
	if (e->key() == Qt::Key_0) {
		scene_id = 0;
		update();
	}
	else if (e->key() == Qt::Key_1) {
		scene_id = 1;
		update();
	}
}

void MyGLWidget::scene_0()
{
	glClear(GL_COLOR_BUFFER_BIT);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0.0f, 100.0f, 0.0f, 100.0f, -1000.0f, 1000.0f);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glTranslatef(50.0f, 50.0f, 0.0f);
	
	//draw a diagonal "I"
	glPushMatrix();
	glColor3f(0.839f, 0.153f, 0.157f);
	glRotatef(45.0f, 0.0f, 0.0f, 1.0f);
	glTranslatef(-2.5f, -22.5f, 0.0f);
	glBegin(GL_TRIANGLES);
	glVertex2f(0.0f, 0.0f);
	glVertex2f(5.0f, 0.0f);
	glVertex2f(0.0f, 45.0f);

	glVertex2f(5.0f, 0.0f);
	glVertex2f(0.0f, 45.0f);
	glVertex2f(5.0f, 45.0f);

	glEnd();
	glPopMatrix();	
}

void MyGLWidget::scene_1()
{
	// 清除颜色缓冲区，将窗口背景设置为当前的清除颜色（通常是黑色）
    glClear(GL_COLOR_BUFFER_BIT);

    // 设置当前矩阵模式为投影矩阵模式
    glMatrixMode(GL_PROJECTION);

    // 将当前矩阵重置为单位矩阵
    glLoadIdentity();

    // 设置正交投影矩阵
    // 参数依次为：左、右、下、上、近、远
    // 这里设置了一个从 (-100, -100) 到 (100, 100) 的二维视图区域，
    // 并且设置深度范围为从 -1000 到 1000
    glOrtho(-100.0f, 100.0f, -100.0f, 100.0f, -1000.0f, 1000.0f);

    // 设置当前矩阵模式为模型视图矩阵模式
    glMatrixMode(GL_MODELVIEW);

    // 将当前矩阵重置为单位矩阵
    glLoadIdentity();

    // 将模型视图矩阵平移到指定位置
    // 这里将模型视图矩阵平移到 (0, 0, 0) 位置
    glTranslatef(0.0f, 0.0f, 0.0f);

    // 注释掉的代码：
    // 如果需要将模型视图矩阵平移到窗口的中心位置，可以使用以下代码：
    // glTranslatef(0.5 * width(), 0.5 * height(), 0.0f);

    // 启用混合以支持透明度
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	// 设置颜色
	// glColor3f(0.0f, 0.0f, 0.0f);


    // 绘制坐标轴
    // 绘制X轴
    glColor3f(0.0f, 0.0f, 0.0f); // 黑色
    glLineWidth(2.0f);
    glBegin(GL_LINES);
    glVertex2f(-100.0f, 0.0f);
    glVertex2f(100.0f, 0.0f);
    glEnd();

    // 绘制Y轴
    glColor3f(0.0f, 0.0f, 0.0f); // 黑色
    glBegin(GL_LINES);
    glVertex2f(0.0f, -100.0f);
    glVertex2f(0.0f, 100.0f);
    glEnd();

    // 绘制中心点
    glPointSize(5.0f);
    glColor3f(1.0f, 0.0f, 0.0f); // 红色
    glBegin(GL_POINTS);
    glVertex2f(0.0f, 0.0f);
    glEnd();

    // 设置填充颜色为半透明黑色
    // glColor4f(0.0f, 0.0f, 0.0f, 0.3f); // 黑色，透明度0.3

    //your implementation here, maybe you should write several glBegin
    // 绘制字母C
    glColor4f(1.0f, 0.0f, 0.0f, 0.4f); // 红色
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-35.0f, 40.0f);
    glVertex2f(-35.0f, 50.0f);
    glVertex2f(-75.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-35.0f, 40.0f);
    glVertex2f(-35.0f, 50.0f);
    glVertex2f(-75.0f, 50.0f);
    glEnd();


    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-65.0f, 40.0f);
    glVertex2f(-65.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-65.0f, 40.0f);
    glVertex2f(-65.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();



    // 下横线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, -50.0f);
    glVertex2f(-35.0f, -50.0f);
    glVertex2f(-35.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, -50.0f);
    glVertex2f(-35.0f, -50.0f);
    glVertex2f(-35.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();

    // 绘制字母J
    glColor4f(1.0f, 1.0f, 0.0f, 0.4f); // 黄色
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(-6.0f, 40.0f);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(5.0f, 50.0f);
    glVertex2f(-6.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-6.0f, 40.0f);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(5.0f, 50.0f);
    glVertex2f(-6.0f, 50.0f);
    glEnd();

    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(15.0f, 40.0f);
    glVertex2f(15.0f, -40.0f);
    glVertex2f(5.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(15.0f, 40.0f);
    glVertex2f(15.0f, -40.0f);
    glVertex2f(5.0f, -40.0f);
    glEnd();

    // 下横线
    glBegin(GL_QUADS);
    glVertex2f(-8.0f, -50.0f);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-8.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-8.0f, -50.0f);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-8.0f, -40.0f);
    glEnd();

    // 连接J的上横线和竖线的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(5.0f, 50.0f);  // 上横线右端
    glVertex2f(5.0f, 40.0f);  // 竖线上端
    glVertex2f(15.0f, 40.0f);    // 竖线右端
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(5.0f, 50.0f);  
    glVertex2f(5.0f, 40.0f);  
    glVertex2f(15.0f, 40.0f);    
    glEnd();

    // J下横线左边的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(-8.0f, -50.0f);  // 下横线左下角
    glVertex2f(-8.0f, -40.0f);  // 下横线左上角
    glVertex2f(-16.0f, -38.0f);    // 钩
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-8.0f, -50.0f); 
    glVertex2f(-8.0f, -40.0f); 
    glVertex2f(-16.0f, -38.0f); 
    glEnd();

    // J下横线右边的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(10.0f, -50.0f);  // 下横线右下角
    glVertex2f(10.0f, -40.0f);  // 下横线右上角
    glVertex2f(15.0f, -40.0f);    // 竖线右下角
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(15.0f, -40.0f);
    glEnd();

    // 绘制字母F
    glColor4f(0.0f, 0.0f, 1.0f, 0.4f); // 蓝色
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(75.0f, 40.0f);
    glVertex2f(75.0f, 50.0f);
    glVertex2f(35.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(75.0f, 40.0f);
    glVertex2f(75.0f, 50.0f);
    glVertex2f(35.0f, 50.0f);
    glEnd();

    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(45.0f, 40.0f);
    glVertex2f(45.0f, -50.0f);
    glVertex2f(35.0f, -50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(45.0f, 40.0f);
    glVertex2f(45.0f, -50.0f);
    glVertex2f(35.0f, -50.0f);
    glEnd();

    // 中横线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 0.0f);
    glVertex2f(70.0f, 0.0f);
    glVertex2f(70.0f, 10.0f);
    glVertex2f(35.0f, 10.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 0.0f);
    glVertex2f(70.0f, 0.0f);
    glVertex2f(70.0f, 10.0f);
    glVertex2f(35.0f, 10.0f);
    glEnd();
	//your implementation
	
	glPopMatrix();
}
```

执行代码后得到的图形如下：

![alt text](image-15.png)

#### 讨论内容

- 比较GL_TRIANGLES,GL_TRIANGLE_STRIP,GL_QUAD_STRIP 的绘制开销（需要的glVertex 调用次数）

  - GL_TRIANGLES（独立三角形）
    每三个顶点构成一个独立的三角形，且不存在顶点共享  
    每个三角形需要 3 次 glVertex 调用，若绘制 N 个三角形，则总共需要 3N 次 glVertex 调用
    - 在`scene_0`中使用如下：
    ```cpp
        // 绘制字母"I"的两个三角形
        glBegin(GL_TRIANGLES);
        glVertex2f(0.0f, 0.0f);
        glVertex2f(5.0f, 0.0f);
        glVertex2f(0.0f, 45.0f);

        glVertex2f(5.0f, 0.0f);
        glVertex2f(0.0f, 45.0f);
        glVertex2f(5.0f, 45.0f);
        glEnd();
    ```
    总计：2个三角形 × 3次 = 6次 glVertex 调用
    - 在`scene_1`中使用如下：
    ```cpp
        // 连接J的上横线和竖线的三角形
        glBegin(GL_TRIANGLES);
        glVertex2f(5.0f, 50.0f);  
        glVertex2f(5.0f, 40.0f);  
        glVertex2f(15.0f, 40.0f);    
        glEnd();

        // J下横线左边的三角形
        glBegin(GL_TRIANGLES);
        glVertex2f(-8.0f, -50.0f);  
        glVertex2f(-8.0f, -40.0f);  
        glVertex2f(-16.0f, -38.0f);    
        glEnd();

        // J下横线右边的三角形
        glBegin(GL_TRIANGLES);
        glVertex2f(10.0f, -50.0f);  
        glVertex2f(10.0f, -40.0f);  
        glVertex2f(15.0f, -40.0f);    
        glEnd();
    ```
    总计：3个三角形 × 3次 = 9次 glVertex 调用
    - 故GL_TRIANGLES 总共：6 + 9 = 15次 glVertex 调用

  - GL_QUADS（独立四边形）
    每四个顶点构成一个独立的四边形，且不存在顶点共享  
    每个四边形需要 4 次 glVertex 调用，若绘制 M 个四边形，则总共需要 4M 次 glVertex 调用
    - 在`scene_1`中使用如下：
    ```cpp
        // 绘制字母C
        // 上横线
        glBegin(GL_QUADS);
        glVertex2f(-75.0f, 40.0f);
        glVertex2f(-35.0f, 40.0f);
        glVertex2f(-35.0f, 50.0f);
        glVertex2f(-75.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_QUADS);
        glVertex2f(-75.0f, 40.0f);
        glVertex2f(-65.0f, 40.0f);
        glVertex2f(-65.0f, -40.0f);
        glVertex2f(-75.0f, -40.0f);
        glEnd();

        // 下横线
        glBegin(GL_QUADS);
        glVertex2f(-75.0f, -50.0f);
        glVertex2f(-35.0f, -50.0f);
        glVertex2f(-35.0f, -40.0f);
        glVertex2f(-75.0f, -40.0f);
        glEnd();

        // 绘制字母J
        // 上横线
        glBegin(GL_QUADS);
        glVertex2f(-6.0f, 40.0f);
        glVertex2f(5.0f, 40.0f);
        glVertex2f(5.0f, 50.0f);
        glVertex2f(-6.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_QUADS);
        glVertex2f(5.0f, 40.0f);
        glVertex2f(15.0f, 40.0f);
        glVertex2f(15.0f, -40.0f);
        glVertex2f(5.0f, -40.0f);
        glEnd();

        // 下横线
        glBegin(GL_QUADS);
        glVertex2f(-8.0f, -50.0f);
        glVertex2f(10.0f, -50.0f);
        glVertex2f(10.0f, -40.0f);
        glVertex2f(-8.0f, -40.0f);
        glEnd();

        // 绘制字母F
        // 上横线
        glBegin(GL_QUADS);
        glVertex2f(35.0f, 40.0f);
        glVertex2f(75.0f, 40.0f);
        glVertex2f(75.0f, 50.0f);
        glVertex2f(35.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_QUADS);
        glVertex2f(35.0f, 40.0f);
        glVertex2f(45.0f, 40.0f);
        glVertex2f(45.0f, -50.0f);
        glVertex2f(35.0f, -50.0f);
        glEnd();

        // 中横线
        glBegin(GL_QUADS);
        glVertex2f(35.0f, 0.0f);
        glVertex2f(70.0f, 0.0f);
        glVertex2f(70.0f, 10.0f);
        glVertex2f(35.0f, 10.0f);
        glEnd();
    ```
    - GL_QUADS 总共：12 + 12 + 12 = 36次 glVertex 调用

  - GL_LINE_LOOP（闭合折线）
    通过连续的顶点构成一个闭合的折线，每两个顶点构成一条线段  
    第一个顶点需要 1 次 glVertex 调用，之后每增加一个顶点，只需 1 次 glVertex 调用 来构成一条新的线段，若绘制 N 个顶点，则总共需要 N 次 glVertex 调用
    - 在`scene_1`中使用如下：
    ```cpp
        // 绘制字母C
        // 上横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(-75.0f, 40.0f);
        glVertex2f(-35.0f, 40.0f);
        glVertex2f(-35.0f, 50.0f);
        glVertex2f(-75.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_LINE_LOOP);
        glVertex2f(-75.0f, 40.0f);
        glVertex2f(-65.0f, 40.0f);
        glVertex2f(-65.0f, -40.0f);
        glVertex2f(-75.0f, -40.0f);
        glEnd();

        // 下横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(-75.0f, -50.0f);
        glVertex2f(-35.0f, -50.0f);
        glVertex2f(-35.0f, -40.0f);
        glVertex2f(-75.0f, -40.0f);
        glEnd();

        // 绘制字母J
        // 上横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(-6.0f, 40.0f);
        glVertex2f(5.0f, 40.0f);
        glVertex2f(5.0f, 50.0f);
        glVertex2f(-6.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_LINE_LOOP);
        glVertex2f(5.0f, 40.0f);
        glVertex2f(15.0f, 40.0f);
        glVertex2f(15.0f, -40.0f);
        glVertex2f(5.0f, -40.0f);
        glEnd();

        // 下横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(-8.0f, -50.0f);
        glVertex2f(10.0f, -50.0f);
        glVertex2f(10.0f, -40.0f);
        glVertex2f(-8.0f, -40.0f);
        glEnd();

        // 连接J的上横线和竖线的三角形
        glBegin(GL_LINE_LOOP);
        glVertex2f(5.0f, 50.0f);  
        glVertex2f(5.0f, 40.0f);  
        glVertex2f(15.0f, 40.0f);    
        glEnd();

        // J下横线左边的三角形
        glBegin(GL_LINE_LOOP);
        glVertex2f(-8.0f, -50.0f); 
        glVertex2f(-8.0f, -40.0f); 
        glVertex2f(-16.0f, -38.0f); 
        glEnd();

        // J下横线右边的三角形
        glBegin(GL_LINE_LOOP);
        glVertex2f(10.0f, -50.0f);
        glVertex2f(10.0f, -40.0f);
        glVertex2f(15.0f, -40.0f);
        glEnd();

        // 绘制字母F
        // 上横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(35.0f, 40.0f);
        glVertex2f(75.0f, 40.0f);
        glVertex2f(75.0f, 50.0f);
        glVertex2f(35.0f, 50.0f);
        glEnd();

        // 竖线
        glBegin(GL_LINE_LOOP);
        glVertex2f(35.0f, 40.0f);
        glVertex2f(45.0f, 40.0f);
        glVertex2f(45.0f, -50.0f);
        glVertex2f(35.0f, -50.0f);
        glEnd();

        // 中横线
        glBegin(GL_LINE_LOOP);
        glVertex2f(35.0f, 0.0f);
        glVertex2f(70.0f, 0.0f);
        glVertex2f(70.0f, 10.0f);
        glVertex2f(35.0f, 10.0f);
        glEnd();
    ```
    - GL_LINE_LOOP 总共：12 + 21 + 12 = 45次 glVertex 调用

---

**剩余部分因为没有在本次代码中使用到，故直接进行分析**

  - GL_TRIANGLE_STRIP（三角形带）
    通过连续的顶点构成一个带状的三角形序列，每添加一个新的顶点，就会与前两个顶点共同构成一个新的三角形  
    第一个三角形需要 3 次 glVertex 调用，之后每增加一个顶点，只需 1 次 glVertex 调用 来构成一个新的三角形，若绘制 N 个三角形，则总共需要 2 + N 次 glVertex 调用（即初始两个顶点 + N 个新的顶点）

  - GL_QUAD_STRIP（四边形带）
    通过连续的顶点构成一个带状的四边形序列，每两个新的顶点与前两个顶点共同构成一个新的四边形  
    前四个顶点构成 2 个四边形，需要 4 次 glVertex 调用，之后每增加两个新的顶点，只需 2 次 glVertex 调用 来构成一个新的四边形，若绘制 M 个四边形，则总共需要 2 + 2(M - 1) = 2M 次 glVertex 调用

---

- 比较以下两个视角下，Orthogonal及Perspective投影方式产生的图像：
  1) 从（0,0,d）看向原点(0,0,0)；
  2) 从(0,0.5*d, d)看向原点(0,0,0)。
  注：可使用(0,1,0)作为视角的上方向（up）

##### 1） 从（0,0,d）看向原点(0,0,0)

具体实现代码如下：

```cpp
#include "myglwidget.h"
#include <QKeyEvent>
#include <GL/glu.h> // 确保链接了GLU库

// 构造函数
MyGLWidget::MyGLWidget(QWidget* parent)
    : QOpenGLWidget(parent),
    scene_id(0),
    projection_mode(ORTHOGONAL), // 初始为正交投影
    d(1000.0f) // 设置观察距离 d
{
}

// 析构函数
MyGLWidget::~MyGLWidget()
{
}

// 初始化 OpenGL
void MyGLWidget::initializeGL()
{
    initializeOpenGLFunctions(); // 初始化OpenGL函数
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f); // 设置清除颜色为白色
    glDisable(GL_DEPTH_TEST); // 初始禁用深度测试
}

// 绘制函数
void MyGLWidget::paintGL()
{
    // 根据当前的投影模式决定是否清除深度缓冲区
    if (scene_id == 1 && projection_mode == PERSPECTIVE) {
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    }
    else {
        glClear(GL_COLOR_BUFFER_BIT);
    }

    if (scene_id == 0) {
        scene_0();
    }
    else {
        // 设置投影方式
        if (projection_mode == ORTHOGONAL) {
            setupOrthogonalProjection();
        }
        else if (projection_mode == PERSPECTIVE) {
            setupPerspectiveProjection();
        }

        scene_1();
    }
}

// 调整视口大小
void MyGLWidget::resizeGL(int width, int height)
{
    glViewport(0, 0, width, height);
    update();
}

// 键盘事件处理
void MyGLWidget::keyPressEvent(QKeyEvent* e) {
    // 按 0 切换到场景0
    if (e->key() == Qt::Key_0) {
        scene_id = 0;
        glDisable(GL_DEPTH_TEST); // 场景0不需要深度测试
        update();
    }
    // 按 1 切换到场景1，并默认使用正交投影
    else if (e->key() == Qt::Key_1) {
        scene_id = 1;
        projection_mode = ORTHOGONAL; // 默认正交投影
        glDisable(GL_DEPTH_TEST); // 正交投影禁用深度测试
        update();
    }
    // 在场景1中，按 O 切换到正交投影
    else if (e->key() == Qt::Key_O && scene_id == 1) {
        projection_mode = ORTHOGONAL;
        glDisable(GL_DEPTH_TEST); // 正交投影禁用深度测试
        update();
    }
    // 在场景1中，按 P 切换到透视投影
    else if (e->key() == Qt::Key_P && scene_id == 1) {
        projection_mode = PERSPECTIVE;
        glEnable(GL_DEPTH_TEST); // 透视投影启用深度测试
        update();
    }
    else {
        QOpenGLWidget::keyPressEvent(e);
    }
}

// 设置正交投影矩阵
void MyGLWidget::setupOrthogonalProjection()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // 设置正交投影参数：左, 右, 下, 上, 近, 远
    glOrtho(-100.0f, 100.0f, -100.0f, 100.0f, -d - 100.0f, d + 100.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    // 从 (0,0,d) 观察原点 (0,0,0)，在正交投影中只需平移
    glTranslatef(0.0f, 0.0f, -d);
}

// 设置透视投影矩阵
void MyGLWidget::setupPerspectiveProjection()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // 设置透视投影参数：视场角（度）, 纵横比, 近裁剪面, 远裁剪面
    gluPerspective(45.0, static_cast<GLdouble>(width()) / height(), 1.0, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    // 使用 gluLookAt 设置视点、目标点和上方向
    gluLookAt(0.0, 0.0, d,  // 观察点位置
        0.0, 0.0, 0.0,  // 目标点
        0.0, 1.0, 0.0); // 上方向
}

// 场景0：绘制旋转的字母 "I"
void MyGLWidget::scene_0()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0f, 100.0f, 0.0f, 100.0f, -1000.0f, 1000.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glTranslatef(50.0f, 50.0f, 0.0f);

    // 绘制一个旋转的字母 "I"
    glPushMatrix();
    glColor3f(0.839f, 0.153f, 0.157f); // 设置颜色
    glRotatef(45.0f, 0.0f, 0.0f, 1.0f); // 旋转45度
    glTranslatef(-2.5f, -22.5f, 0.0f); // 平移

    glBegin(GL_TRIANGLES);
    // 第一个三角形
    glVertex2f(0.0f, 0.0f);
    glVertex2f(5.0f, 0.0f);
    glVertex2f(0.0f, 45.0f);

    // 第二个三角形
    glVertex2f(5.0f, 0.0f);
    glVertex2f(0.0f, 45.0f);
    glVertex2f(5.0f, 45.0f);
    glEnd();
    glPopMatrix();
}

// 场景1：绘制坐标轴和字母 "C", "J", "F"
void MyGLWidget::scene_1()
{
    // 绘制坐标轴
    // 绘制X轴
    glColor3f(0.0f, 0.0f, 0.0f); // 黑色
    glLineWidth(2.0f);
    glBegin(GL_LINES);
    glVertex2f(-100.0f, 0.0f);
    glVertex2f(100.0f, 0.0f);
    glEnd();

    // 绘制Y轴
    glColor3f(0.0f, 0.0f, 0.0f); // 黑色
    glBegin(GL_LINES);
    glVertex2f(0.0f, -100.0f);
    glVertex2f(0.0f, 100.0f);
    glEnd();

    // 绘制中心点
    glPointSize(5.0f);
    glColor3f(1.0f, 0.0f, 0.0f); // 红色
    glBegin(GL_POINTS);
    glVertex2f(0.0f, 0.0f);
    glEnd();

    // 启用混合以支持透明度
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    // 绘制字母C
    glColor4f(1.0f, 0.0f, 0.0f, 0.4f); // 红色，半透明
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-35.0f, 40.0f);
    glVertex2f(-35.0f, 50.0f);
    glVertex2f(-75.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-35.0f, 40.0f);
    glVertex2f(-35.0f, 50.0f);
    glVertex2f(-75.0f, 50.0f);
    glEnd();

    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-65.0f, 40.0f);
    glVertex2f(-65.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, 40.0f);
    glVertex2f(-65.0f, 40.0f);
    glVertex2f(-65.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();

    // 下横线
    glBegin(GL_QUADS);
    glVertex2f(-75.0f, -50.0f);
    glVertex2f(-35.0f, -50.0f);
    glVertex2f(-35.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-75.0f, -50.0f);
    glVertex2f(-35.0f, -50.0f);
    glVertex2f(-35.0f, -40.0f);
    glVertex2f(-75.0f, -40.0f);
    glEnd();

    // 绘制字母J
    glColor4f(1.0f, 1.0f, 0.0f, 0.4f); // 黄色，半透明
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(-6.0f, 40.0f);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(5.0f, 50.0f);
    glVertex2f(-6.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-6.0f, 40.0f);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(5.0f, 50.0f);
    glVertex2f(-6.0f, 50.0f);
    glEnd();

    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(15.0f, 40.0f);
    glVertex2f(15.0f, -40.0f);
    glVertex2f(5.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(15.0f, 40.0f);
    glVertex2f(15.0f, -40.0f);
    glVertex2f(5.0f, -40.0f);
    glEnd();

    // 下横线
    glBegin(GL_QUADS);
    glVertex2f(-8.0f, -50.0f);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-8.0f, -40.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-8.0f, -50.0f);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(-8.0f, -40.0f);
    glEnd();

    // 连接J的上横线和竖线的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(5.0f, 50.0f);  // 上横线右端
    glVertex2f(5.0f, 40.0f);  // 竖线上端
    glVertex2f(15.0f, 40.0f); // 竖线右端
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(5.0f, 50.0f);
    glVertex2f(5.0f, 40.0f);
    glVertex2f(15.0f, 40.0f);
    glEnd();

    // J下横线左边的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(-8.0f, -50.0f);  // 下横线左下角
    glVertex2f(-8.0f, -40.0f);  // 下横线左上角
    glVertex2f(-16.0f, -38.0f); // 钩
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(-8.0f, -50.0f);
    glVertex2f(-8.0f, -40.0f);
    glVertex2f(-16.0f, -38.0f);
    glEnd();

    // J下横线右边的三角形
    glBegin(GL_TRIANGLES);
    glVertex2f(10.0f, -50.0f);  // 下横线右下角
    glVertex2f(10.0f, -40.0f);  // 下横线右上角
    glVertex2f(15.0f, -40.0f);  // 竖线右下角
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(10.0f, -50.0f);
    glVertex2f(10.0f, -40.0f);
    glVertex2f(15.0f, -40.0f);
    glEnd();

    // 绘制字母F
    glColor4f(0.0f, 0.0f, 1.0f, 0.4f); // 蓝色，半透明
    // 上横线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(75.0f, 40.0f);
    glVertex2f(75.0f, 50.0f);
    glVertex2f(35.0f, 50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(75.0f, 40.0f);
    glVertex2f(75.0f, 50.0f);
    glVertex2f(35.0f, 50.0f);
    glEnd();

    // 竖线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(45.0f, 40.0f);
    glVertex2f(45.0f, -50.0f);
    glVertex2f(35.0f, -50.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 40.0f);
    glVertex2f(45.0f, 40.0f);
    glVertex2f(45.0f, -50.0f);
    glVertex2f(35.0f, -50.0f);
    glEnd();

    // 中横线
    glBegin(GL_QUADS);
    glVertex2f(35.0f, 0.0f);
    glVertex2f(70.0f, 0.0f);
    glVertex2f(70.0f, 10.0f);
    glVertex2f(35.0f, 10.0f);
    glEnd();
    glBegin(GL_LINE_LOOP);
    glVertex2f(35.0f, 0.0f);
    glVertex2f(70.0f, 0.0f);
    glVertex2f(70.0f, 10.0f);
    glVertex2f(35.0f, 10.0f);
    glEnd();
}
```

在本代码中，添加了设置正交投影函数`setupOrthogonalProjection`和设置透视投影`setupPerspectiveProjection`函数，并且添加了键盘事件处理，通过按键 `0` 切换到 `scene_0`，按键 `1` 切换到 `scene_1`，并默认使用`正交投影`，在 `scene_1` 中，按键 `O` 切换到`正交投影`，按键 `P` 切换到`透视投影`

正交投影和透视投影的运行结果如下所示：

![alt text](image-20.png)
![alt text](image-21.png)

在正交投影中，物体的大小不会随距离的变化而变化，而透视投影中，物体的大小会随着距离的增加而变小，因此，在透视投影中，字母CJF的大小会随着距离的增加而变小，而正交投影中，字母CJF的大小不会变化

##### 2） 从(0,0.5*d, d)看向原点(0,0,0)

修改代码中的`setupPerspectiveProjection`函数，将`gluLookAt`函数的第一个参数修改为`(0.0, 0.5*d, d)`，然后修改`setupOrthogonalProjection`函数，将`gluLookAt`函数的参数修改为`(0, -0.5f * d, -d)`，运行程序，具体实现如下：

```cpp
// 设置正交投影矩阵
void MyGLWidget::setupOrthogonalProjection()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // 设置正交投影参数：左, 右, 下, 上, 近, 远
    glOrtho(-100.0f, 100.0f, -100.0f, 100.0f, -d - 100.0f, d + 100.0f);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    // 从 (0,0,d) 观察原点 (0,0,0)，在正交投影中只需平移
    glTranslatef(0.0f, -0.5f * d, -d);
}

// 设置透视投影矩阵
void MyGLWidget::setupPerspectiveProjection()
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    // 设置透视投影参数：视场角（度）, 纵横比, 近裁剪面, 远裁剪面
    gluPerspective(45.0, static_cast<GLdouble>(width()) / height(), 1.0, 1000.0);

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    // 使用 gluLookAt 设置视点、目标点和上方向
    gluLookAt(0.0, 0.5 * d, d,  // 观察点位置
        0.0, 0.0, 0.0,  // 目标点
        0.0, 1.0, 0.0); // 上方向
}
```

运行结果如下所示：

![alt text](image-18.png)
![alt text](image-19.png)

更换观察点后，可以看到透视投影会有明显的上大下小的效果，而正交投影则没有这种效果，只是以不同的方向，看到大小完全相同的字母

### 绘制立体姓氏首字母

- 在三维空间内，以原点为绘制中心，绘制立体的姓氏首字母

参考了linux字符画中字母`C`的绘制方式，拼接了多个立方体和衔接的三棱柱，并采用线条框架和内部填充颜色的绘制方式（本来想选择渐变色，但是因为顶点过多导致代码段过长，最终只选择了不同透明度下不同颜色的完全填充）

![C](./img/C.png)

按键部分实现代码如下：

```cpp
// 键盘事件处理
void MyGLWidget::keyPressEvent(QKeyEvent* e) {
    // 按 0 切换到场景0
    if (e->key() == Qt::Key_0) {
        scene_id = 0;
        glDisable(GL_DEPTH_TEST); // 场景0不需要深度测试
        update();
    }
    // 按 1 切换到场景1，并默认使用正交投影
    else if (e->key() == Qt::Key_1) {
        scene_id = 1;
        projection_mode = ORTHOGONAL; // 默认正交投影
        glDisable(GL_DEPTH_TEST); // 正交投影禁用深度测试
        update();
    }

    // 在场景1中，按 O 切换到正交投影
    else if (e->key() == Qt::Key_O && scene_id == 1) {
        projection_mode = ORTHOGONAL;
        glDisable(GL_DEPTH_TEST); // 正交投影禁用深度测试
        update();
    }
    // 在场景1中，按 P 切换到透视投影
    else if (e->key() == Qt::Key_P && scene_id == 1) {
        projection_mode = PERSPECTIVE;
        glEnable(GL_DEPTH_TEST); // 透视投影启用深度测试
        update();
    }
    else if (e->key() == Qt::Key_2) {
        scene_id = 2; // 切换到scene2
        update();
    }
    else if (e->key() == Qt::Key_Q && scene_id == 2) {
        rotation_x -= 10.0f; // 绕x轴顺时针旋转
        update();
    }
    else if (e->key() == Qt::Key_A && scene_id == 2) {
        rotation_x += 10.0f; // 绕x轴逆时针旋转
        update();
    }
    else if (e->key() == Qt::Key_W && scene_id == 2) {
        rotation_y -= 10.0f; // 绕y轴顺时针旋转
        update();
    }
    else if (e->key() == Qt::Key_S && scene_id == 2) {
        rotation_y += 10.0f; // 绕y轴逆时针旋转
        update();
    }
    else if (e->key() == Qt::Key_E && scene_id == 2) {
        rotation_z -= 10.0f; // 绕z轴顺时针旋转
        update();
    }
    else if (e->key() == Qt::Key_D && scene_id == 2) {
        rotation_z += 10.0f; // 绕z轴逆时针旋转
        update();
    }
    else {
        QOpenGLWidget::keyPressEvent(e);
    }
}
```

- 代码解释：默认进入场景0，按1进入场景1，按2进入场景2，在场景1中，按O切换到正交投影，按P切换到透视投影，在场景2中，按Q、A、W、S、E、D分别绕X、Y、Z轴顺时针、逆时针旋转

---

绘制的结果如下图所示：

#### 正视图（未旋转）

![alt text](image-22.png)

---

#### 绕X轴旋转（设计为按键q为顺时针旋转，按键a为逆时针旋转）

![alt text](image-23.png)

![alt text](image-24.png)

---

#### 绕Y轴旋转（设计为按键w为顺时针旋转，按键s为逆时针旋转）

![alt text](image-25.png)

![alt text](image-26.png)

---

#### 绕Z轴旋转（设计为按键e为顺时针旋转，按键d为逆时针旋转）

![alt text](image-27.png)

![alt text](image-28.png)

---

#### 综合XYZ轴的旋转

![alt text](image-29.png)

![alt text](image-30.png)