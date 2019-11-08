# rgb2graynresize_csv
RGB image to gray image and resize image and save csv file

read all of file in your floder and if it is 'jpg' then change image to csv file.  

해당 폴더에 있는 모든 파일을 읽어서 .jpg 파일인지 구분한 다음에 이미지 파일일 경우에는 gray 이미지로 변경한 후, csv 파일로 저장하는 코드


Example
- rgb2gray_resize_csv('Folder/Path', row, col);
- rgb2gray_resize_csv('폴더경로', 이미지 가로, 이미지 세로);



Version
- v2 : save image data together in a one csv file.
