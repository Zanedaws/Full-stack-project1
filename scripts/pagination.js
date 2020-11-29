$(document).ready(function(){
    var cards = $(".card");
    console.log(cards);
    var i;
    for( i = 5; i < cards.length; i++)
    {
        $("#"+cards[i].id).hide();
    }
    $(".pageButton").click(function(){
        let lowBound = parseInt(this.id) * 5;
        let upBound = (parseInt(this.id) + 1) * 5;
        let cards = $(".card");
        var i;
        for(i = 0; i < cards.length; i++)
        {
            if(i >= lowBound && i < upBound)
            {
                $("#"+cards[i].id).show();
            }
            else
            {
                $("#"+cards[i].id).hide();
            }
        }
    });
});