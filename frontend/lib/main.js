
const ing_endpoint = "https://students.mimuw.edu.pl/~mo430007/bad_cocktail/api/app.cgi/ingredients";
const drinks_search_endpoint = "https://students.mimuw.edu.pl/~mo430007/flask/app.cgi/drinks?";
const drink_endpoint = "https://students.mimuw.edu.pl/~mo430007/flask/app.cgi/drink?";

/* ==================================================== Autocomplete section ===================================== */


class Components_selector {
    selected_items = {};
    possible_items;
    all_items;
    
    constructor() {}
    
    async init() {
        var components = await getComponents();
        this.possible_items = {};
        for (var component of components) {
            this.possible_items[component.name] = (component.id);
        }
        this.all_items = this.possible_items;
        autocomplete(document.getElementById('component-search'), Object.keys(this.possible_items));
    }

    selected_ids() {
        var out = [];
        for (var el of Object.values(this.selected_items)) {
            out.push(el);
        }
        return out;
    }
    
    addEntity(entity) {
        if(!(entity in this.possible_items)) return;
        this.selected_items[entity] = this.possible_items[entity];
        delete this.possible_items[entity];
        this.resetList();
    }
    
    removeEntity(entity) {
        if(!(entity in this.selected_items)) return;
        this.possible_items[entity] = this.selected_items[entity];
        delete this.selected_items[entity];
        this.resetList();
    }

    resetItems() {
        for(var el of Object.keys(this.selected_items)) {
            this.possible_items[el] = this.selected_items[el];
            delete this.selected_items[el];
        }
        this.resetList();
    }
    
    resetList() {
        document.getElementById("selection").innerHTML = "";
        for (var el of Object.keys(this.selected_items)) {
            var li = document.createElement("li");
            li.setAttribute("class", "selected-item");
            li.innerHTML = el + '<i class="far fa-trash-alt remove-icon mx-2"></i>';
            li.data = el;
            li.addEventListener("click", removeComponent);
            document.getElementById("selection").appendChild(li);
        }
        autocomplete(document.getElementById('component-search'), Object.keys(this.possible_items));
    }
}

var comp_sel = new Components_selector();
comp_sel.init();

function removeComponent(e) {
    comp_sel.removeEntity(this.data);
}

async function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    function check(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items pb-5");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase() || (val.length == 0)) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    comp_sel.addEntity(this.getElementsByTagName("input")[0].value);
                    inp.value = "";
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    };
    inp.addEventListener("input", check);
    inp.addEventListener("focus", check);
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40 || e.keyCode == 9) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            e.preventDefault();
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            } else {
                if(this.value in comp_sel.possible_items) {
                    comp_sel.addEntity(this.value);
                    inp.value = "";
                    /*close the list of autocompleted values,
                    (or any other open lists of autocompleted values:*/
                    closeAllLists();
                }
            }
        }
    });
    function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
    }
    function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
    }
    function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

async function getComponents() {
    var out;
    var lol = await fetch(ing_endpoint, {method: 'GET',headers: {
            'Content-Type': 'application/json'
            }
        });
    await lol.json().then(data => {out = data});
    return out;
}

/* ========================================================= End of Autocomplete ============================= */

function populateTemplate(templateAsString, values){
    for(var key in values){
        if(values.hasOwnProperty(key) && key != "ingridients"){
            templateAsString = templateAsString.replace("{"+key+"}", values[key]);
        }
    }
    return templateAsString;
}

function fetchIngCount() {
    var countDOM = document.getElementById("component-count");
    var count = countDOM.value;
    countDOM.value = 0;
    return parseInt(count);
}

async function sendSearchform() {
    var out;
    var search_params = new URLSearchParams();
    search_params.append("ids", comp_sel.selected_ids());
    search_params.append("count", fetchIngCount());
    var lol = await fetch(drinks_search_endpoint + search_params.toString(), {
        method: 'GET'});
    await lol.json().then(data => {out = data});
    return out;
}

async function search() {
    var response = await sendSearchform();
    document.getElementById("drink-list").innerHTML = "";
    for(var drink of response) {
        var new_card = document.createElement("div");
        new_card.innerHTML = populateTemplate(document.getElementById("card-template").innerHTML, drink);
        document.getElementById("drink-list").appendChild(new_card);
        var ing_list = new_card.getElementsByClassName("ing-list")[0];
        for(var ing of drink.ingridients) {
            var new_ing = document.createElement("li");
            new_ing.innerHTML = ing
            ing_list.appendChild(new_ing);
        }
        new_card.addEventListener("click",drink_click(drink.id));
    }
    comp_sel.resetItems();
}

document.getElementById("search-btn").addEventListener("click", search);

async function getDrinkInfo(id) {
    var out;
    var search_params = new URLSearchParams();
    search_params.append("id", id)
    var lol = await fetch(drink_endpoint, {method: 'GET',headers: {
            'Content-Type': 'application/json'
            }
        });
    await lol.json().then(data => {out = data});
    return out;
}

async function renderDrinkInfo(id) {
    var drinkInfo = await getDrinkInfo(id);
    document.getElementById("modal-title").innerHTML = drinkInfo.name;
    document.getElementById("modal-recipe").innerHTML = drinkInfo.recipe;
    var ing_list = document.getElementById("modal-ing");
    ing_list.innerHTML = "";
    for(var ing of drinkInfo.ingridients) {
        var new_ing = document.createElement("li");
        new_ing.innerHTML = ing
        ing_list.appendChild(new_ing);
    }
    document.getElementById("modal-img").src = drinkInfo.image_link;
    document.getElementById("modal-glassware").src = drinkInfo.glassware;
}

function drink_click(id) {
    return function(e) {
        renderDrinkInfo(id);
    };
}