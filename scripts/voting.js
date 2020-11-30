$(document).ready(function(){

    var votes;

    $.get("/"+window.location.pathname.split("/")[1]+"/votes", function(data){
       votes = (data.votes);
       console.log(votes);
       var cards= $(".card");
       var j;
       var k;
       for(j = 0; j < cards.length; j++)
       {
           for(k = 0; k < votes.length; k++)
           {
               if(cards[j].id == votes[k][1])
               {
                   let val = $(cards[j]).children("#buttonContainer").children(".likes").html();
                   val = parseInt(val);
                   if(votes[k][2] == "up")
                    val++;
                   else
                    val--;
                   $(cards[j]).children("#buttonContainer").children(".likes").html(val);
               }
           }
       }
    });





    $(".likeButton").click(function(){

        let div = $(this).parents("div")[1];
        var i;
        for(i = 0; i < votes.length; i++)
        {
            if(window.location.pathname.split("/")[1] == votes[i][0])
                if(div.id == votes[i][1])
                    return;
        }
        $.post("/"+window.location.pathname.split("/")[1]+"/"+div.id+"/"+this.id+"/votes");
        let curVal = parseInt($("#"+div.id).children("#buttonContainer").children(".likes").html());
        if(this.id == "up")
            curVal++;
        else
            curVal--;
        $("#"+div.id).children("#buttonContainer").children(".likes").html(curVal);
        $.get("/"+window.location.pathname.split("/")[1]+"/votes", function(data){
            votes = (data.votes);
        });
    });
});