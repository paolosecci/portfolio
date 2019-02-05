//TEAM 1
var select1; //declare reference to select element 1
var t1s = 0; //team 1 score
var t1n = "";//team 1 name
//TEAM 2
var select2; //declare reference to select element 2
var t2s = 0; //team 2 score
var t2n = "";//team 2 name

var teams = ["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"];
var get_full_name = {"ATL": "Atlanta Hawks","BKN": "Brooklyn Nets","BOS": "Boston Celtics","CHA": "Charolette Hornets","CHI": "Chicago Bulls","CLE": "Cleveland Caveliers","DAL": "Dallas Mavericks","DEN": "Denver Nuggets","DET": "Detroit Pistons","GSW": "Golden State Warriors","HOU": "Houston Rockets","IND": "Indiana Pacers","LAC": "Los Angeles Clippers","LAL": "Los Angeles Lakers","MEM": "Memphis Grizzlies","MIA": "Miami Heat","MIL": "Milwaukee Bucks","MIN": "Minnesota Timberwolves","NOP": "New Orleans Pelicans","NYK": "New York Knicks","OKC": "Oklahoma City Thunder","ORL": "Orlando Magic","PHI": "Philedelphia 76ers","PHX": "Phoenix Suns","POR": "Portland Trail Blazers","SAC": "Sacramento Kings","SAS": "San Antonio Spurs","TOR": "Toronto Raptors","UTA": "Utah Jazz","WAS": "Washington Wizards"};

function init(){
    //initialize reference to select elements
    select1 = d3.select("#selDataset");
    select2 = d3.select("#selDataset2");
    
    teams.forEach(function(team){
        select1.append("option")
            .text(team).property("value", team);
        select2.append("option")
            .text(team).property("value", team);
    });
}

//called on optionChange
function playerStats1(team){
    t1n = team;
    d3.json(`/predict/${team}`).then((data)=>{
        //d3 to select panels
        var PANELname = d3.select("#player-name");
        var PANELstat = d3.select("#player-data");
        var PANELteam = d3.select("#team-data");
        
        //clear any existing panel displays
        PANELname.html("");
        PANELstat.html("");
        PANELteam.html("");
        
        //use `Object.entries` to display player statistics
        Object.entries(data[1]).forEach((player)=>{
            PANELname.append("h6").text(`${player[1]['NAME']}`);
            PANELstat.append("h6").text(`PTS: ${player[1]['PTS']} AST: ${player[1]['AST']} REB: ${player[1]['REB']}`);
        });
        
        //user-feedback
        PANELteam.append("h6").text('waiting for opponent...');
    });
}
function playerStats2(team){
    t2n = team;
    d3.json(`/predict/${team}`).then((data)=>{
        //d3 to select panels
        var PANELname = d3.select("#player-name2");
        var PANELstat = d3.select("#player-data2");
        var PANELteam = d3.select("#team-data2");
        
        //clear any existing panel displays
        PANELname.html("");
        PANELstat.html("");
        PANELteam.html("");
        
        //use `Object.entries` to display player statistics
        Object.entries(data[1]).forEach((player)=>{
            PANELname.append("h6").text(`${player[1]['NAME']}`);
            PANELstat.append("h6").text(`PTS: ${player[1]['PTS']} AST: ${player[1]['AST']} REB: ${player[1]['REB']}`);
        });
        
        //user-feedback
        PANELteam.append("h6").text("building matchups...");
        d3.select("#team-data").html("").append("h6").text("building matchups...")
    });
}
function optionChanged1(new_team){playerStats1(new_team);}
function optionChanged2(new_team){playerStats2(new_team);}

function winningteam(){
    console.log("here")
    d3.json(`/simgame/${t1n}/${t2n}`).then(function(api_response){
        //get predicted scores from api
        t1s = api_response[0];
        t2s = api_response[1];
        
        //get references to team output panels
        var PANELt1 = d3.select("#team-data");
        var PANELt2 = d3.select("#team-data2");
        
        //display scores to team output panels
        PANELt1.html("").append("h1").text(Math.round(t1s));
        PANELt2.html("").append("h1").text(Math.round(t2s));
        
        //log result to console
        console.log(t1n, ": ", t1s);
        console.log(t2n, ": ", t2s); 
        
        //chose winner
        if(t1s > t2s){winningteam = t1n;}
        else{winningteam = t2n;}
        
        //display winner
        var PANELchamp = d3.select("#winningteam");
        PANELchamp.html("")
            .append("img")
                .attr("src", "../static/img/logos/" + winningteam + "_logo.svg")
                .attr("width", 400).attr("height", 400)
            .append("h1").text(get_full_name[winningteam]);
    });                               
}

d3.selectAll("#calc").on("click", winningteam);
init();