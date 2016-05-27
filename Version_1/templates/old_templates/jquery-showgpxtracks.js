/*! jQuery Gpx Viewer - v0.2.0 - 2014-11-10
* Copyright (c) 2014 kssfilo; Licensed MIT */
(function($){

	var gpxHandler=function(self,r,gpxurl){
		var minheight=200;
		var infowidth=30;

		var k=$('<div style="width:100%;height:70%">');
		var g=$('<canvas style="width:100%;height:20%">');
		var f=$('<div style="width:100%;height:10%;font-size:12px">');
		k.appendTo(self);
		g.appendTo(self);
		f.appendTo(self);

		var c=g[0].getContext('2d');
		g[0].width=g[0].offsetWidth;
		g[0].height=g[0].offsetHeight;
		var cw=g[0].width-infowidth;
		var aw=g[0].width;
		cw=aw;
		var ch=g[0].height;

		var map = new google.maps.Map(k[0]);
		map.setOptions({
			scrollwheel: true,
			draggable: true,
			panControl:true,
			mapTypeId: google.maps.MapTypeId.HYBRID
			//mapTypeId: google.maps.MapTypeId.TERRAIN
		});
		var pt=[];
		var nlt=0;
		var slt=90;
		var wlg=180;
		var elg=0;
		var lev=100000;
		var hev=0;
		var dt=0;
		var lps=null;
		var acc=0;
		var dsc=0;
		for(var i=0;i<r.length;i++){
				if(i>0){r[i].ev=r[i-1].ev*0.9+r[i].ev*0.1;}
				
				nlt=r[i].lt>nlt?r[i].lt:nlt;
				slt=r[i].lt<slt?r[i].lt:slt;
				wlg=r[i].lg<wlg?r[i].lg:wlg;
				elg=r[i].lg>elg?r[i].lg:elg;
				lev=Math.min(r[i].ev,lev);
				hev=Math.max(r[i].ev,hev);
				var cps=new google.maps.LatLng(r[i].lt,r[i].lg);
				pt.push(cps);
				if(i!==0){
					var ldt=google.maps.geometry.spherical.computeDistanceBetween(cps,lps);
					dt+=ldt;
					r[i].dt=dt;
					if(r[i-1].ev<r[i].ev){acc+=r[i].ev-r[i-1].ev;}
					if(r[i-1].ev>r[i].ev){dsc+=r[i-1].ev-r[i].ev;}
				}
				lps=cps;
		}
		var dev=hev-lev;
		dev=Math.max(dev,minheight);

		var pl=new google.maps.Polyline({
			path:pt,
			strokeColor:"#FF0000",
			strokeWeight:2,
			strokeOpacity:0.9,
		});
		pl.setMap(map);

		var b=new google.maps.LatLngBounds(new google.maps.LatLng(slt,wlg),new google.maps.LatLng(nlt,elg));
		map.fitBounds(b);

		var dx=cw/dt;
		var dy=ch/dev;

		c.fillStyle='white';
		c.fillRect(0,0,cw,ch);

		c.strokeStyle='lightgray';
		c.lineWidth=1;
		for(i=0;i<4;i++){
			c.beginPath();
			c.moveTo(0,ch/4*i);
			c.lineTo(cw-1,ch/4*i);
			c.closePath();
			c.stroke();
		}
		
		c.fillStyle='black';
		c.beginPath();
		c.moveTo(cw-1,ch-1);
		c.lineTo(0,ch-1);
		c.lineTo(0,ch-1-(r[0].ev-lev)*dy);
		for(i=1;i<r.length;i++){
			c.lineTo(dx*r[i].dt-1,ch-1-dy*(r[i].ev-lev));
		}
		c.lineTo(cw-1,ch-1);
		c.closePath();
		c.fill();

		c.strokeStyle='black';
		c.lineWidth=2;
		c.strokeRect(1,1,cw-2,ch-2);

		c.fillStyle='blue';
		c.textAlign='left';
		c.font="12px Ariel";
		c.shadowBlur=1;
		c.shadowColor="white";
		c.fillText("+"+Math.round(dev)+"m",5,16);
		c.fillText(""+Math.round(lev)+"m",5,ch-6);

		var s="Distance:"+Math.round(dt)/1000+"km/Low:"+Math.round(lev)+"m/High:"+Math.round(hev)+"m/Accent:+"+Math.round(acc)+"m/Descent:"+Math.round(dsc)+"m";
		if(gpxurl){s+="[<a href='"+gpxurl+"' download>Download GPX</a>]";}
		s+=" (c)<a href='http://kanasys.com/gtech/'>kanasys.com</a>";
		f.html(s);
	};

	$.fn.showGpxTracksString=function(gpx){
		this.each(function(){
			var self=this;
			var xml=$.parseXML(gpx);

			var track=[];
			$(xml).find("trkpt").each(function() {
				var tm=new Date($(this).find('time').text());
				track.push({lt:parseFloat($(this).attr('lat')),lg:parseFloat($(this).attr('lon')),ev:parseFloat($(this).find('ele').text()),tm:tm});
			});
			gpxHandler(self,track);
		});
	};

	$.fn.showGpxTracks=function(optionalUrl){
		this.each(function(){
			var self=this;
			var gpxurl=optionalUrl;
			if(!gpxurl){gpxurl=$(this).attr('src');}
			if(!gpxurl){return;}

			function loadGpx(gpxurl,cb){
				$.ajax({	
					url:gpxurl,
					type:'GET',
					dataType:'xml',
					timeout:20000,
					error:function(e) {
						console.log(e);
						return;
					},
					success:function(xml){
						var track=[];
						$(xml).find("trkpt").each(function() {
							var tm=new Date($(this).find('time').text());
							track.push({lt:parseFloat($(this).attr('lat')),lg:parseFloat($(this).attr('lon')),ev:parseFloat($(this).find('ele').text()),tm:tm});
						});
						if(track.length>1){cb(self,track,gpxurl);}
					}
				});
			}

			loadGpx(gpxurl,gpxHandler);
		});
	};
})(jQuery);
