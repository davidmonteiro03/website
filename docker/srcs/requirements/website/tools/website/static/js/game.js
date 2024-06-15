function startGame() {
	myGameArea.start();
  }

  var myGameArea = {
	canvas : document.createElement("canvas"),
	start : function() {
	  this.canvas.width = 480;
	  this.canvas.height = 270;
	  this.context = this.canvas.getContext("2d");
	  app.insertBefore(this.canvas, app.childNodes[0]);
	}
  }
