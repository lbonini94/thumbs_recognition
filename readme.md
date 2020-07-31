# Thumbs UP/DOWN/LEFT/RIGHT recognition project :thumbsup: 
 
**:warning: This content is highly based on [this project](https://github.com/greatsharma/Thumb-Gestures-Detection) :warning:**   

---

## How to run this project

### Option 1 (Anaconda)

- Create a environment with `conda create --name myenv --file spec-file.txt`
- Activate environment
- go to ~/app and run `python app.py`
- arguments in section below are avaliable for this option

### Option 2 (Docker)

- Download image with `docker pull lbonini94/thumbs_recognition`
  - OR build with Dockerfile using `docker build -t <my_container_name> .`

#### Arguments you can use

- `-mode 'debug'` (optional)
- `-ip 'http://10.0.0.101:8080/video'` #For CAMERA IP. :calling: You can try with [this app](https://play.google.com/store/apps/details?id=com.pas.webcam&hl=pt).
  - remove `--device /dev/video0:/dev/video0` from `docker run` command below
  - add `-ip 'http://10.0.0.101:8080/video'` (Your address is different) after app.py 
- `-camera 0` (optional)  #If you don't use your main camera, pass `-camera 1`
  - change `--device /dev/video0:/dev/video0` to `--device /dev/video1:/dev/video1`

:persevere: **Docker only works with IP Camera** :sweat:

```
docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=$DISPLAY \
--user=$(id -u $USER):$(id -g $USER) \
--env QT_X11_NO_MITSHM=1 \
lbonini94/thumbs_recognition /usr/local/bin/python app.py -ip 'http://10.0.0.101:8080/video'
```

### To-do

- [x] Pre-trained CNN model for thumbs up and down (plus: left and right)
- [ ] Train model again with different parameters and new pictures
- [ ] Share webcam device with docker container 