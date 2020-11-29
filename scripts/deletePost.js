$(document).ready(function(){
    $(".delete").click(function(){
        let divID = this.id.replace("/","");
        if(confirm("Are you sure?"))
        {
            $("#" + divID).remove();
            $.post("/"+divID+"/delete");
            let cards = $(".card");
            let visCards = $(".card:visible");
            let lowBound;
            var i;
            for(i = 0; i < cards.length; i++)
            {
                if(visCards[0].id == cards[i].id)
                {
                    lowBound = i;
                }
            }
            console.log(cards.length);
            let upBound = lowBound + 5;
            var k;
            for(k = 0; k < cards.length; k++)
            {
                if(k >= lowBound && k < upBound)
                {
                    $("#"+cards[k].id).show();
                }
                else
                {
                    $("#"+cards[k].id).hide();
                }
            }
            let pageButtons = $(".pageButton");
            if(pageButtons.length > Math.ceil(cards.length/5))
            {
                $(".pageButton").last().remove();
            }
        }
    });
});