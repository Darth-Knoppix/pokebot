var rndSeed;

var bot;
var renderReady = false;

function preload() {
  bot = new bot();
  bot.preload();
}

function setup () {
  var main_canvas = createCanvas(440, 220);
  main_canvas.parent('canvasContainer');

  rndSeed = random(1024);
  bot.setup();
}

function keyTyped() {
  if (key == '!') {
    saveBlocksImages();
  }
  else if (key == '@') {
    saveBlocksImages(true);
  }
}

function reportRenderReady() {
  finalDiv = createDiv('(render ready)');  
  finalDiv.id("render_ready")
}

function draw() {
  background(204);
  // randomSeed(0);
  resetFocusedRandom(rndSeed);
  message = bot.respond();
  var text = select('#tweet_text');
  text.html(message);
  if(renderReady == false) {
    if(bot.isDone()) {
      reportRenderReady();
      renderReady = true;
    }
  }
}
