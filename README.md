# 每日早安推送给别人家的女朋友

> 由于此项目是在小红书开放教程的，因此不便更新代码。我会起一个闭源的仓库，用于赚钱（不是），用于真正零代码做一个早安的推送。大概预计周二晚跟大家见面，我会在小红书上更新，有需要的可以稍微等等。不过这个是要收费的，我用自己的服务器帮大家推送，10块钱应该不多吧。。

首发在小红书，但是有大家说字看不清，因此在这里搞一篇使用说明。

效果如图。当然，文字是可以修改的。
![5e72e89fd7ff692a0bfa62010517c0c](https://user-images.githubusercontent.com/9566402/183242263-c93517a2-5377-435d-8386-8d47252c9e07.jpg)

首先，按图搜索，测试号，进来之后微信扫码登录！
![cf7dbd4502df44765ed3506f55caea5](https://user-images.githubusercontent.com/9566402/183242272-134e37e7-718d-42dd-9ed7-fca2810e94e6.png)

按图点击 Use this template，创建到自己的仓库下！
![e6581c43572b00b12c1a82ca8d7178b](https://user-images.githubusercontent.com/9566402/183242340-2ef26c63-1ca1-420e-abd4-8672c25d61c9.png)


按下图，创建模板，设置变量，把微信公众平台上的各种字符串按说明创建到 GitHub -> Settings -> Secrets -> Actions 中。
![71bf9d11a876d23ef0f0728645a8ba0](https://user-images.githubusercontent.com/9566402/183242301-fd6ab30e-bfe5-4245-b2a9-f690184db307.png)
![381e8ee4a7c5ec6b8c09719f2c7e486](https://user-images.githubusercontent.com/9566402/183242295-4dcf06bb-2083-4883-8745-0af753ca805c.png)
![48c60750cec7adc546e0ad99e3082b3](https://user-images.githubusercontent.com/9566402/183242320-18500adc-14e5-4522-a3ad-ae19cc4479bf.png)

启用自己项目下的 Action！
![30a5b1b2b06ba4a40a3d8ef01652409](https://user-images.githubusercontent.com/9566402/183242334-9943c538-ba3d-4d01-8377-d040143b7560.png)

如果运行出现错误，按以下方法可以看到错误，在这里 issue 提问也可以，在小红书问也可以
![6b0da6f44e18c2bfd94910c377d13e6](https://user-images.githubusercontent.com/9566402/183242349-1aa5ada6-2ee7-4cf9-a542-4b2dad88b8fe.png)

启用后可以直接运行，看看女朋友的手机有没有收到推送吧！
这个定时任务是每天早晨8点推送，如果会编程的同学可以自己自定义一些东西～

图中的操作，除了各种英文字符串不一样，模板消息中的中文不一样，其他的应该都是一样的，不然程序跑不通的～

Github 的右上角可以点击 star 给我点鼓励吧亲

小红书上点点关注，点点赞，有什么好玩的东西可以at我，我来教你们做
