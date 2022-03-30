## hand-tracking-droid
### quick setup
First of all download these two libraries and add it to your arduino ide also setup the ide according to esp32cam requirements
- [AsyncTCP Library](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbjl3eUFXM3IwbWNUemxpQXJfbThxR2NaYWo4Z3xBQ3Jtc0ttOGZUcENfdnlST3puWkdpZEFlUUtrWVNuYmpDZW80a0pCZXZIampLUzhzUlBiOUNCS1J6TldmVHFnZDU2WktHUG8tbVNFOTkyUWhyRWJOUTMtMU1OYjViRnl0bktpeG9heHRDczVGWW5nWmdSQjRIWQ&q=https%3A%2F%2Fgithub.com%2Fme-no-dev%2FAsyncTCP%2Farchive%2Frefs%2Fheads%2Fmaster.zip)
- [ESPAsyncWebServer Library](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqazJ0dVdtZ1Y2cnkxY1cyWUFtQVZTSm9waVV1UXxBQ3Jtc0trY2FXWmtzT0pOZVJDcERLSW55UGlUV0hXNkU1WHRiWHY0cWtlTzVCX3BJMWxrdFpDQU81WDlnVVlrbXF2dkJGYTRBQktmbnN1cFhLMWE0NXV2aXo3dXY0NDhvX3NLaGxSOXY0bHpGVzdWRVdWUHZzUQ&q=https%3A%2F%2Fgithub.com%2Fme-no-dev%2FESPAsyncWebServer%2Farchive%2Frefs%2Fheads%2Fmaster.zip)

after adding upload the sketch i provided to your esp32 camera module
update your wifi creds in that code before uploading
![code](https://github.com/zerocool-11/hand-tracking-droid/wifi.png)

install all the python deps using this command
```
pip install -r requirements.txt
```

after that find the ip address of your esp32 cam and update it to the python code that's it
then simply run main-espcam.py script and enjoy

