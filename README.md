![](https://cloud.githubusercontent.com/assets/1134738/18608819/7046281e-7d11-11e6-8274-378f5855637d.png)

---

### Introduction
SAIL (Speech Assisted Interface Library) is a library (duh!) that will make your application much more accessible, in the most simplest way you can think of... **speech**. You can let your users talk to the application as if it were an actual person, thanks to the beauty of Machine Learning, and let a whole variety of new users to literally converse with your application.

#### This is how easy we've made it... all you need to incorporate our library is:
* Add the dependencies
```` compile ‘com.dark.sail:1.0.0’ ````
* Create an object of Sailboat and call the initialize function, where you can specify the different actions and views on the current activity. ```` Sailboat sailboat = new Sailboat();  
sailboat.initialize(Context, ArrayList); ````
* Were you expecting a third step? There isn't ;)
