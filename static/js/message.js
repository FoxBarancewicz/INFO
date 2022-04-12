var a;
function show_hide()
{
    if(a==1)
        {
            document.getElementsByClassName("recieved-chats").style.display="inline";
            return a = 0;
        }
    else
        {
            document.getElementsByClassName("recieved-chats").style.display="none";
            return a = 1;
        }
}