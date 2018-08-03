
----------------------------------------
|context> => |context: breakfast menu>

supported-ops |menu: breakfast> => |op: >
 |menu: breakfast> => |food: Belgian Waffles> + |food: Strawberry Belgian Waffles> + |food: Berry-Berry Belgian Waffles> + |food: French Toast> + |food: Homestyle Breakfast>

supported-ops |food: Belgian Waffles> => |op: name> + |op: price> + |op: description> + |op: calories>
name |food: Belgian Waffles> => |text: "Belgian Waffles">
price |food: Belgian Waffles> => |price: 5.95>
description |food: Belgian Waffles> => |text: "Two of our famous Belgian Waffles with plenty of real maple syrup">
calories |food: Belgian Waffles> => |calories: 650>

supported-ops |food: Strawberry Belgian Waffles> => |op: name> + |op: price> + |op: description> + |op: calories>
name |food: Strawberry Belgian Waffles> => |text: "Strawberry Belgian Waffles">
price |food: Strawberry Belgian Waffles> => |price: 7.95>
description |food: Strawberry Belgian Waffles> => |text: "Light Belgian waffles covered with strawberries and whipped cream">
calories |food: Strawberry Belgian Waffles> => |calories: 900>

supported-ops |food: Berry-Berry Belgian Waffles> => |op: name> + |op: price> + |op: description> + |op: calories>
name |food: Berry-Berry Belgian Waffles> => |text: "Berry-Berry Belgian Waffles">
price |food: Berry-Berry Belgian Waffles> => |price: 8.95>
description |food: Berry-Berry Belgian Waffles> => |text: "Light Belgian waffles covered with an assortment of fresh berries and whipped cream">
calories |food: Berry-Berry Belgian Waffles> => |calories: 900>

supported-ops |food: French Toast> => |op: name> + |op: price> + |op: description> + |op: calories>
name |food: French Toast> => |text: "French Toast">
price |food: French Toast> => |price: 4.50>
description |food: French Toast> => |text: "Thick slices made from our homemade sourdough bread">
calories |food: French Toast> => |calories: 600>

supported-ops |food: Homestyle Breakfast> => |op: name> + |op: price> + |op: description> + |op: calories>
name |food: Homestyle Breakfast> => |text: "Homestyle Breakfast">
price |food: Homestyle Breakfast> => |price: 6.95>
description |food: Homestyle Breakfast> => |text: "Two eggs, bacon or sausage, toast, and our ever-popular hash browns">
calories |food: Homestyle Breakfast> => |calories: 950>

 |food: waffles> => |word: waffles>  
 |country: Belgium> => |word: belgian> 
 |food: strawberries> => |word: strawberries> 
 |fruit: strawberries> => |word: strawberries>
 |food: berries> => |word: berries>   
 |fruit: berries> => |word: berries> 
 |country: France> => |word: french> 
 |food: toast> => |word: toast> 
 |meal: breakfast> => |word: breakfast> 
 |food: egg> => |word: egg>
 |food: eggs> => |word: eggs> 
 |food: bacon> => |word: bacon> 
 |food: sausage> => |word: sausage> 
 |food: sausages> => |word: sausages>
 |number: 2> => |word: two> 
 |food: cream> => |word: cream> 
 |food: belgian waffles> => |word: belgian> . |word: waffles>
 |food: maple syrup> => |word: maple> . |word: syrup>
 |food: whipped cream> => |word: whipped> . |word: cream>
 |food: hash browns> => |word: hash> . |word: browns>
----------------------------------------
