# whoisinmyphoto: A photo organizer that organizes photos using face recognition technology

The fully working webpage is now available at [whoisinmyphoto.com](https://www.whoisinmyphoto.com)
<p align="center">
  <img src="https://miro.medium.com/max/915/1*XknCwHJ88MvR0RznnHP47Q.png">
</p>

## Steps:
1. Open the webpage [whoisinmyphoto.com](https://www.whoisinmyphoto.com)
2. Click “Start with making folders of your friends and family!”
3. Click “Choose Files” and upload a folder with multiple images of people (for demo, make sure to upload a folder that we provided for the assignment: ObamaFamilyImage or Avengers from Image Folders for Testing)
4. Click “Upload” to upload the images (wait until the loading ends)
5. Go to next page by clicking green “Next” button
6. Click “Choose Files” and upload a folder with distinct image of each people who will show up in your webpage (for demo, make sure to upload a folder that we provided: EachObamaMember or AvengersName from Image Folders for Testing)
7. Click “Upload” to upload the images (wait until the loading ends)
8. Go to next page by clicking green “Next” button (The loading may take up to 5 minutes, so please be patient)
9. Click “Download” text to download the organized folder with subfolders of names of the people
10. All done! Check the zip file whether every image seems to be organized correctly!

## What to do when errors come up:
1. (For most problems) Click the “Reset” button at the end of each page to reset all the data uploaded or entered data and start again from the home page of [whoisinmyphoto.com](https://www.whoisinmyphoto.com)
2. The webpage may give errors between annotation page and classify page because of the long time duration from our face recognition model. If so, please go back to the home page [whoisinmyphoto.com](https://www.whoisinmyphoto.com) and go to the next page and click the reset button. This will delete all the information entered by you and you can start over the service with no problem.
3. If there is an error during a demo due to deviation from steps above that is not solved with the “Reset” button, please let us know so that we can renew the service.

## Example directories (or folders) to upload
1. For uploads page<br/>
<p align="center">
  <img src="https://www.whoisinmyphoto.com/static/ScreenShotObamaFamilyImage.png" width="698" height="506">
</p>
2. For annotations page
<p align="center">
  <img src="https://www.whoisinmyphoto.com/static/ScreenShotEachObamaMember.png" width="628" height="346">
</p>

## Result of our service
Our webpage generates zip file for our users when the users press download button.
1. General view of a folder when the zip file is decompressed
<p align="center">
  <img src="/example/screenshot_organized_folder.png" width="500" height="250">
</p>
2. Folder 1

3. Folder 2

4. Folder 3

5. Folder 4

## Face recognition model
Our face recognition is based on [FaceNet](https://arxiv.org/abs/1503.03832) model which consists of [Inception-Resnet-v1](https://arxiv.org/abs/1602.07261) (pretrained on [VGGFace2](https://arxiv.org/abs/1710.08092)) and [MTCNN (Multi-task Cascaded Convolutional Networks)](https://arxiv.org/abs/1604.02878)
