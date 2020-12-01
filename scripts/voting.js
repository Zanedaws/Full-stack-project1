$(document).ready(function(){

    var votes;
    var userVotes = [];
    var userHash = window.location.pathname.split("/")[1];

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
               if(votes[k][0] == userHash)
               {
                   userVotes.push(votes[k]);
               }
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
        console.log(userVotes);

        let div = $(this).parents("#buttonContainer").parents(".card"); //gets jquery object for card
        let p = $(this).parents("#buttonContainer").children(".likes"); //gets jquery object for paragraph
        let divObj = div[0]; //gets the actual HTML div thing
        var realVote = null;

        var i;
        for(i = 0; i < userVotes.length; i++)
        {
            if(divObj.id == userVotes[i][1])
            {
                console.log("found real vote");
                realVote = userVotes[i];
                break;
            }
            console.log("not real vote");
        }
        console.log(realVote);
        if(realVote == null)
        {
            console.log("No Vote has been made.");
            $.post("/"+userHash+"/"+divObj.id+"/"+this.id+"/votes");
            userVotes.push([userHash,divObj.id,this.id]);
            let curVal = parseInt(p.html());
            if(this.id == "up")
                curVal++;
            else
                curVal--;
            p.html(curVal);
        }
        else
        {
            if(this.id === realVote[2])
            {
                console.log("Vote already made.");
                return;
            }
            $.post("/"+userHash+"/"+divObj.id+"/"+this.id+"/votes");
            userVotes[i][2] = this.id;
            let curVal = parseInt(p.html());
            if(this.id == "up")
                curVal += 2;
            else
                curVal -= 2;
            p.html(curVal);
        }

    });


//    $(".likeButton").click(function(){
//
//        let div = $(this).parents("div")[1];
//        var i;
//        for(i = 0; i < votes.length; i++)
//        {
//            if(window.location.pathname.split("/")[1] == votes[i][0])
//                if(div.id == votes[i][1])
//                    if((this.id == "up" && votes[i][2] == "up") || (this.id == "down" && votes[i][2] == "down"))
//                    {
//                        console.log(this.id);
//                        console.log(votes[i][2]);
//                        return;
//                    }
//                    else
//                    {
//                        let curVal = parseInt($("#"+div.id).children("#buttonContainer").children(".likes").html());
//                        if(this.id == "up")
//                            curVal++;
//                        else
//                            curVal--;
//                        $("#"+div.id).children("#buttonContainer").children(".likes").html(curVal);
//                    }
//        }
//        $.post("/"+window.location.pathname.split("/")[1]+"/"+div.id+"/"+this.id+"/votes");
//        let curVal = parseInt($("#"+div.id).children("#buttonContainer").children(".likes").html());
//        if(this.id == "up")
//            curVal++;
//        else
//            curVal--;
//        $("#"+div.id).children("#buttonContainer").children(".likes").html(curVal);
//        $.get("/"+window.location.pathname.split("/")[1]+"/votes", function(data){
//            votes = (data.votes);
//        });
//    });
});