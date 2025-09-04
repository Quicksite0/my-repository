canvas=document.getElementById("myCanvas")
color="red"
ctx=canvas.getContext("2d")
ctx.beginPath()
ctx.strokeStyle = color;
ctx.lineWidth = 2;
ctx.arc(200, 40 ,0 ,2 * Math.PI );
ctx.stroke();
mouse_x = e.clientX
mouse_y = e.clientY