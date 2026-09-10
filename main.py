<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>제동거리 시뮬레이터</title>
<style>
  :root{
    --bg: #14171a;
    --panel: #1c2024;
    --panel-2: #21262b;
    --line: #2c3238;
    --text: #eceae4;
    --text-dim: #8b929a;
    --yellow: #ffb703;
    --red: #e5383b;
    --teal: #4cc9c0;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    background:var(--bg);
    color:var(--text);
    font-family:-apple-system, "Segoe UI", "Pretendard", "Noto Sans KR", Helvetica, Arial, sans-serif;
    line-height:1.5;
    padding:28px 20px 60px;
  }
  .mono{ font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }
  .app{max-width:1180px;margin:0 auto;}
  header{margin-bottom:24px;}
  header h1{
    font-size:26px;
    font-weight:700;
    letter-spacing:-0.01em;
    margin:0 0 6px;
  }
  header p{
    margin:0;
    color:var(--text-dim);
    font-size:14.5px;
  }
  .dashboard{
    display:grid;
    grid-template-columns:280px 1fr;
    gap:18px;
  }
  .panel{
    background:var(--panel);
    border:1px solid var(--line);
    border-radius:6px;
    padding:20px;
  }
  .panel h2{
    font-size:13px;
    font-weight:600;
    color:var(--text-dim);
    margin:0 0 16px;
    padding-bottom:10px;
    border-bottom:1px solid var(--line);
  }
  .field{margin-bottom:20px;}
  .field label{
    display:block;
    font-size:13px;
    color:var(--text-dim);
    margin-bottom:8px;
  }
  .field input[type="number"]{
    width:100%;
    background:var(--panel-2);
    border:1px solid var(--line);
    border-radius:4px;
    color:var(--text);
    font-size:15px;
    padding:9px 10px;
  }
  .field input[type="number"]:focus{outline:2px solid var(--yellow); outline-offset:1px;}
  .field select{
    width:100%;
    background:var(--panel-2);
    border:1px solid var(--line);
    border-radius:4px;
    color:var(--text);
    font-size:15px;
    padding:9px 10px;
  }
  .field select:focus{outline:2px solid var(--yellow); outline-offset:1px;}
  .field .unit-tag{
    display:inline-block;
    margin-left:8px;
    font-size:12px;
    color:var(--text-dim);
  }
  .field .err{
    display:none;
    color:var(--red);
    font-size:12px;
    margin-top:6px;
  }
  .field.invalid .err{display:block;}
  .field.invalid input{border-color:var(--red);}
  .speed-row{
    display:flex;
    align-items:baseline;
    justify-content:space-between;
    margin-bottom:8px;
  }
  .speed-row .val{
    font-size:20px;
    font-weight:700;
    color:var(--yellow);
  }
  .speed-row .val span{font-size:13px; color:var(--text-dim); font-weight:400;}
  input[type="range"]{
    width:100%;
    accent-color:var(--yellow);
  }
  .range-scale{
    display:flex;
    justify-content:space-between;
    font-size:11px;
    color:var(--text-dim);
    margin-top:4px;
  }
  button.run{
    width:100%;
    background:var(--yellow);
    color:#1a1a1a;
    border:none;
    border-radius:4px;
    padding:12px;
    font-weight:700;
    font-size:14.5px;
    cursor:pointer;
    margin-top:6px;
  }
  button.run:disabled{
    background:#4a4d51;
    color:#8a8d91;
    cursor:not-allowed;
  }
  button.run:not(:disabled):hover{background:#ffc93d;}

  .results{margin-top:22px; padding-top:18px; border-top:1px solid var(--line);}
  .result-item{
    display:flex;
    justify-content:space-between;
    align-items:baseline;
    padding:7px 0;
    font-size:13px;
    color:var(--text-dim);
  }
  .result-item b{
    color:var(--text);
    font-size:15px;
    font-weight:700;
  }

  .main-panel{display:flex; flex-direction:column; gap:18px;}

  .track-wrap{padding:20px;}
  .track-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:14px;
    flex-wrap:wrap;
    gap:10px;
  }
  .track-header h2{margin:0; padding:0; border:none;}
  .live-readouts{display:flex; gap:26px;}
  .live-readouts .item{text-align:right;}
  .live-readouts .item .label{font-size:11px; color:var(--text-dim);}
  .live-readouts .item .value{
    font-size:19px;
    font-weight:700;
  }
  .live-readouts .speed-value{color:var(--yellow);}
  .live-readouts .pos-value{color:var(--teal);}

  .road-track{
    position:relative;
    height:78px;
    background:#2a2e33;
    border-radius:4px;
    overflow:hidden;
  }
  .road-track::after{
    content:"";
    position:absolute;
    top:50%;
    left:0; right:0;
    height:2px;
    transform:translateY(-50%);
    background-image:repeating-linear-gradient(to right, #545a60 0, #545a60 22px, transparent 22px, transparent 44px);
  }
  .skid{
    position:absolute;
    left:0; bottom:14px;
    height:6px;
    width:0;
    border-radius:3px;
    background:linear-gradient(to right, rgba(229,56,59,0), rgba(229,56,59,0.85));
  }
  .car{
    position:absolute;
    left:0; top:8px;
    font-size:30px;
    transform:translateX(0);
    line-height:1;
  }
  .car-icon{
    display:inline-block;
    transform:scaleX(-1);
  }
  .track-scale{
    display:flex;
    justify-content:space-between;
    font-size:11px;
    color:var(--text-dim);
    margin-top:8px;
  }

  .charts-wrap{
    display:grid;
    grid-template-columns:repeat(auto-fit, minmax(280px, 1fr));
    gap:18px;
  }
  .chart-box{padding:18px;}
  .chart-box h3{
    font-size:13.5px;
    font-weight:600;
    margin:0 0 12px;
    color:var(--text);
  }
  .chart-box canvas{
    width:100%;
    height:220px;
    display:block;
  }

  .formula-panel{grid-column:1 / -1;}
  .formula-panel h2{margin-bottom:14px;}
  .eq-list{
    display:flex;
    flex-direction:column;
    gap:10px;
    font-size:13.5px;
  }
  .eq-list .eq{
    display:grid;
    grid-template-columns:170px 1fr;
    gap:14px;
    padding:8px 0;
    border-bottom:1px dashed var(--line);
  }
  .eq-list .eq:last-child{border-bottom:none;}
  .eq-list .eq .name{color:var(--text-dim); font-size:13px;}
  .eq-list .eq .expr .sub{color:var(--yellow); font-weight:700;}
  .note{
    margin-top:16px;
    font-size:12.5px;
    color:var(--text-dim);
    border-left:2px solid var(--line);
    padding-left:12px;
  }

  @media (max-width: 900px){
    .dashboard{grid-template-columns:1fr;}
    .charts-wrap{grid-template-columns:1fr;}
    .eq-list .eq{grid-template-columns:1fr;}
  }

</style>
</head>
<body>
<div class="app">
  <header>
    <h1>제동거리 시뮬레이터</h1>
    <p>초기 속력과 자동차 질량을 설정하면 제동거리와 시간에 따른 속력·위치 변화를 계산합니다.</p>
  </header>

  <div class="dashboard">
    <aside class="panel">
      <h2>조건 설정</h2>

      <div class="field" id="massField">
        <label for="massInput">자동차 질량</label>
        <div>
          <input type="number" id="massInput" value="1500" min="1" step="10" class="mono">
          <span class="unit-tag">kg</span>
        </div>
        <div class="err">질량은 0보다 큰 값이어야 합니다.</div>
      </div>

      <div class="field">
        <div class="speed-row">
          <label style="margin-bottom:0;">초기 속력</label>
          <span class="val mono" id="speedLabel">100<span> km/h</span></span>
        </div>
        <input type="range" id="speedSlider" min="1" max="300" step="1" value="100">
        <div class="range-scale mono"><span>1 km/h</span><span>300 km/h</span></div>
      </div>

      <div class="field">
        <label for="speedMultiplier">애니메이션 배속</label>
        <select id="speedMultiplier">
          <option value="0.5">0.5×</option>
          <option value="1" selected>1×</option>
          <option value="2">2×</option>
          <option value="4">4×</option>
          <option value="8">8×</option>
        </select>
      </div>

      <button class="run" id="runBtn">제동 시작</button>

      <div class="results">
        <div class="result-item"><span>감속도 a</span><b class="mono" id="resA">-- m/s²</b></div>
        <div class="result-item"><span>제동 시간 t</span><b class="mono" id="resT">-- s</b></div>
        <div class="result-item"><span>제동거리 d</span><b class="mono" id="resD">-- m</b></div>
      </div>
    </aside>

    <main class="main-panel">
      <section class="panel track-wrap">
        <div class="track-header">
          <h2>제동 애니메이션</h2>
          <div class="live-readouts">
            <div class="item">
              <div class="label">현재 속력 (km/h)</div>
              <div class="value speed-value mono" id="liveSpeed">--</div>
            </div>
            <div class="item">
              <div class="label">이동 거리 (m)</div>
              <div class="value pos-value mono" id="livePos">--</div>
            </div>
          </div>
        </div>
        <div class="road-track" id="roadTrack">
          <div class="skid" id="skid"></div>
          <div class="car" id="car"><span class="car-icon">🚗</span></div>
        </div>
        <div class="track-scale mono"><span>0 m</span><span id="trackEnd">-- m</span></div>
      </section>

      <section class="charts-wrap">
        <div class="panel chart-box">
          <h3>속력–시간 그래프 (km/h vs s)</h3>
          <canvas id="speedChart"></canvas>
        </div>
        <div class="panel chart-box">
          <h3>위치–시간 그래프 (m vs s)</h3>
          <canvas id="positionChart"></canvas>
        </div>
        <div class="panel chart-box">
          <h3>제동거리–속력 그래프 (m vs km/h)</h3>
          <canvas id="distanceChart"></canvas>
        </div>
      </section>
    </main>

    <section class="panel formula-panel">
      <h2>사용한 식 (계산 과정)</h2>
      <div class="eq-list mono" id="eqList">
        <div class="eq"><div class="name">① 마찰력</div><div class="expr">f = μ × m × g</div></div>
        <div class="eq"><div class="name">② 감속도</div><div class="expr">a = f / m = μ × g</div></div>
        <div class="eq"><div class="name">③ 속도 단위 변환</div><div class="expr">v₀(m/s) = v₀(km/h) ÷ 3.6</div></div>
        <div class="eq"><div class="name">④ 제동 시간</div><div class="expr">t_stop = v₀ / a</div></div>
        <div class="eq"><div class="name">⑤ 속력(t)</div><div class="expr">v(t) = v₀ − a·t  (0 ≤ t ≤ t_stop)</div></div>
        <div class="eq"><div class="name">⑥ 위치(t)</div><div class="expr">x(t) = v₀·t − ½·a·t²</div></div>
        <div class="eq"><div class="name">⑦ 제동거리</div><div class="expr">d = v₀² / (2a)</div></div>
      </div>
      <div class="note">
        g = 9.8 m/s², μ = 0.7 로 고정되어 있습니다. 마찰력 f = μmg 에서 감속도 a = f/m = μg 이므로,
        질량 m은 계산 과정에는 등장하지만 최종 감속도·제동거리 값에는 영향을 주지 않습니다
        (반응 시간, 노면 상태 변화, ABS 등 다른 요인은 고려하지 않은 단순 마찰 모델입니다).
      </div>
    </section>
  </div>
</div>

<script>
(function(){
  "use strict";

  var G = 9.8;
  var MU = 0.7;

  var massInput = document.getElementById('massInput');
  var massField = document.getElementById('massField');
  var speedSlider = document.getElementById('speedSlider');
  var speedLabel = document.getElementById('speedLabel');
  var runBtn = document.getElementById('runBtn');
  var speedMultiplierSelect = document.getElementById('speedMultiplier');
  var playbackSpeed = parseFloat(speedMultiplierSelect.value);

  var resA = document.getElementById('resA');
  var resT = document.getElementById('resT');
  var resD = document.getElementById('resD');

  var liveSpeed = document.getElementById('liveSpeed');
  var livePos = document.getElementById('livePos');
  var trackEnd = document.getElementById('trackEnd');

  var roadTrack = document.getElementById('roadTrack');
  var car = document.getElementById('car');
  var skid = document.getElementById('skid');

  var eqList = document.getElementById('eqList');

  var speedCanvas = document.getElementById('speedChart');
  var positionCanvas = document.getElementById('positionChart');
  var distanceCanvas = document.getElementById('distanceChart');

  var animId = null;
  var lastChartData = null;
  var currentSpeedKmh = parseFloat(speedSlider.value);

  function fmt(n, d){
    if(isNaN(n)) return '--';
    return Number(n).toLocaleString('ko-KR', {minimumFractionDigits:d, maximumFractionDigits:d});
  }

  function validateMass(){
    var m = parseFloat(massInput.value);
    var valid = !isNaN(m) && m > 0;
    massField.classList.toggle('invalid', !valid);
    runBtn.disabled = !valid;
    return valid;
  }

  massInput.addEventListener('input', validateMass);

  speedMultiplierSelect.addEventListener('change', function(){
    playbackSpeed = parseFloat(speedMultiplierSelect.value);
  });

  speedSlider.addEventListener('input', function(){
    speedLabel.innerHTML = speedSlider.value + '<span> km/h</span>';
    currentSpeedKmh = parseFloat(speedSlider.value);
    refreshDistanceChart();
  });

  function resizeCanvasForDPR(canvas){
    var dpr = window.devicePixelRatio || 1;
    var rect = canvas.getBoundingClientRect();
    var w = Math.max(rect.width, 260);
    var h = Math.max(rect.height, 180);
    canvas.width = Math.round(w * dpr);
    canvas.height = Math.round(h * dpr);
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { ctx: ctx, w: w, h: h };
  }

  function drawLineChart(canvas, xs, ys, opts){
    var setup = resizeCanvasForDPR(canvas);
    var ctx = setup.ctx, W = setup.w, H = setup.h;
    ctx.clearRect(0, 0, W, H);

    var padL = 46, padR = 12, padT = 12, padB = 30;
    var plotW = W - padL - padR;
    var plotH = H - padT - padB;

    var xMax = Math.max.apply(null, xs.concat([0.1]));
    var rawYMax = Math.max.apply(null, ys.concat([1]));
    var yMax = rawYMax * 1.15;

    ctx.strokeStyle = '#2c3238';
    ctx.fillStyle = '#8b929a';
    ctx.font = '11px SFMono-Regular, Consolas, Menlo, monospace';
    ctx.lineWidth = 1;

    var yTicks = 4;
    for(var i = 0; i <= yTicks; i++){
      var yVal = yMax * i / yTicks;
      var yPix = padT + plotH - (yVal / yMax) * plotH;
      ctx.beginPath();
      ctx.moveTo(padL, yPix);
      ctx.lineTo(padL + plotW, yPix);
      ctx.stroke();
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';
      ctx.fillText(yVal.toFixed(yMax < 10 ? 1 : 0), padL - 6, yPix);
    }

    var xTicks = 5;
    for(var j = 0; j <= xTicks; j++){
      var xVal = xMax * j / xTicks;
      var xPix = padL + (xVal / xMax) * plotW;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      ctx.fillText(xVal.toFixed(2), xPix, padT + plotH + 6);
    }

    ctx.save();
    ctx.translate(12, padT + plotH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#eceae4';
    ctx.fillText(opts.yLabel, 0, 0);
    ctx.restore();

    ctx.textAlign = 'center';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#eceae4';
    ctx.fillText(opts.xLabel || '시간 t (s)', padL + plotW / 2, H - 2);

    if(xs.length > 0){
      ctx.beginPath();
      for(var k = 0; k < xs.length; k++){
        var px = padL + (xs[k] / xMax) * plotW;
        var py = padT + plotH - (ys[k] / yMax) * plotH;
        if(k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.strokeStyle = opts.color;
      ctx.lineWidth = 2.5;
      ctx.lineJoin = 'round';
      ctx.stroke();
    }

    if(opts.marker){
      var mx = padL + (opts.marker.x / xMax) * plotW;
      var my = padT + plotH - (opts.marker.y / yMax) * plotH;

      ctx.save();
      ctx.setLineDash([4, 4]);
      ctx.strokeStyle = '#eceae4';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(mx, padT);
      ctx.lineTo(mx, my);
      ctx.lineTo(padL, my);
      ctx.stroke();
      ctx.restore();

      ctx.beginPath();
      ctx.arc(mx, my, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#eceae4';
      ctx.fill();
      ctx.beginPath();
      ctx.arc(mx, my, 3, 0, Math.PI * 2);
      ctx.fillStyle = opts.color;
      ctx.fill();

      if(opts.marker.label){
        ctx.font = 'bold 12px SFMono-Regular, Consolas, Menlo, monospace';
        ctx.fillStyle = '#eceae4';
        ctx.textBaseline = 'bottom';
        ctx.textAlign = mx > padL + plotW * 0.6 ? 'right' : 'left';
        ctx.fillText(opts.marker.label, mx + (ctx.textAlign === 'right' ? -8 : 8), my - 6);
      }
    }
  }

  function updateCharts(times, speedsKmh, positions){
    lastChartData = { times: times, speedsKmh: speedsKmh, positions: positions };
    drawLineChart(speedCanvas, times, speedsKmh, { color: '#ffb703', yLabel: '속력 v (km/h)' });
    drawLineChart(positionCanvas, times, positions, { color: '#4cc9c0', yLabel: '위치 x (m)' });
  }

  var FIXED_A = MU * G;

  function buildDistanceCurve(){
    var xs = [];
    var ys = [];
    var steps = 150;
    for(var i = 0; i <= steps; i++){
      var vKmh = 300 * i / steps;
      var vMs = vKmh / 3.6;
      var d = (vMs * vMs) / (2 * FIXED_A);
      xs.push(vKmh);
      ys.push(d);
    }
    return { xs: xs, ys: ys };
  }

  var distanceCurve = buildDistanceCurve();

  function refreshDistanceChart(){
    var vMs = currentSpeedKmh / 3.6;
    var d = (vMs * vMs) / (2 * FIXED_A);
    drawLineChart(distanceCanvas, distanceCurve.xs, distanceCurve.ys, {
      color: '#e5383b',
      yLabel: '제동거리 d (m)',
      xLabel: '속력 v₀ (km/h)',
      marker: { x: currentSpeedKmh, y: d, label: fmt(currentSpeedKmh,0) + ' km/h → ' + fmt(d,1) + ' m' }
    });
  }

  window.addEventListener('resize', function(){
    if(lastChartData){
      updateCharts(lastChartData.times, lastChartData.speedsKmh, lastChartData.positions);
    } else {
      drawLineChart(speedCanvas, [0], [0], { color: '#ffb703', yLabel: '속력 v (km/h)' });
      drawLineChart(positionCanvas, [0], [0], { color: '#4cc9c0', yLabel: '위치 x (m)' });
    }
    refreshDistanceChart();
  });

  function updateFormula(v){
    var rows = [
      ['① 마찰력', 'f = ' + MU + ' × ' + fmt(v.mass,0) + ' × ' + G + ' = <span class="sub">' + fmt(v.friction,1) + ' N</span>'],
      ['② 감속도', 'a = ' + fmt(v.friction,1) + ' / ' + fmt(v.mass,0) + ' = <span class="sub">' + fmt(v.a,2) + ' m/s²</span>'],
      ['③ 속도 단위 변환', 'v₀ = ' + fmt(v.v0kmh,1) + ' ÷ 3.6 = <span class="sub">' + fmt(v.v0,2) + ' m/s</span>'],
      ['④ 제동 시간', 't_stop = ' + fmt(v.v0,2) + ' / ' + fmt(v.a,2) + ' = <span class="sub">' + fmt(v.tStop,2) + ' s</span>'],
      ['⑤ 속력(t)', 'v(t) = ' + fmt(v.v0,2) + ' − ' + fmt(v.a,2) + '·t  (0 ≤ t ≤ ' + fmt(v.tStop,2) + ')'],
      ['⑥ 위치(t)', 'x(t) = ' + fmt(v.v0,2) + '·t − ½ × ' + fmt(v.a,2) + '·t²'],
      ['⑦ 제동거리', 'd = ' + fmt(v.v0,2) + '² / (2 × ' + fmt(v.a,2) + ') = <span class="sub">' + fmt(v.brakingDistance,2) + ' m</span>']
    ];
    var html = '';
    for(var i = 0; i < rows.length; i++){
      html += '<div class="eq"><div class="name">' + rows[i][0] + '</div><div class="expr">' + rows[i][1] + '</div></div>';
    }
    eqList.innerHTML = html;
  }

  function runSimulation(){
    if(!validateMass()) return;
    if(animId) cancelAnimationFrame(animId);

    var mass = parseFloat(massInput.value);
    var v0kmh = parseFloat(speedSlider.value);
    var v0 = v0kmh / 3.6;
    var friction = MU * mass * G;
    var a = friction / mass;
    var tStop = a > 0 ? v0 / a : 0;
    var brakingDistance = (v0 * v0) / (2 * a);

    var steps = 120;
    var times = [];
    var speedsKmh = [];
    var positions = [];
    for(var i = 0; i <= steps; i++){
      var t = tStop * i / steps;
      var v = Math.max(v0 - a * t, 0);
      var x = v0 * t - 0.5 * a * t * t;
      times.push(t);
      speedsKmh.push(v * 3.6);
      positions.push(x);
    }
    if(tStop === 0){
      times = [0];
      speedsKmh = [0];
      positions = [0];
    }

    updateCharts(times, speedsKmh, positions);
    currentSpeedKmh = v0kmh;
    refreshDistanceChart();

    resA.textContent = fmt(a,2) + ' m/s²';
    resT.textContent = fmt(tStop,2) + ' s';
    resD.textContent = fmt(brakingDistance,2) + ' m';
    trackEnd.textContent = fmt(brakingDistance,2) + ' m';

    updateFormula({mass: mass, v0kmh: v0kmh, v0: v0, a: a, friction: friction, tStop: tStop, brakingDistance: brakingDistance});

    var trackWidth = roadTrack.clientWidth - 34;
    var maxV0 = 300 / 3.6;
    var maxDistance = (maxV0 * maxV0) / (2 * a);
    car.style.transform = 'translateX(0px)';
    skid.style.width = '0px';

    if(tStop <= 0){
      liveSpeed.textContent = fmt(0,1);
      livePos.textContent = fmt(0,2);
      return;
    }

    var lastFrameTime = null;
    var virtualElapsed = 0;
    function frame(now){
      if(lastFrameTime === null) lastFrameTime = now;
      var deltaSec = (now - lastFrameTime) / 1000;
      lastFrameTime = now;
      virtualElapsed += deltaSec * playbackSpeed;

      var t = Math.min(virtualElapsed, tStop);
      var v = Math.max(v0 - a * t, 0);
      var x = v0 * t - 0.5 * a * t * t;
      var ratio = maxDistance > 0 ? Math.min(x / maxDistance, 1) : 0;
      var px = ratio * trackWidth;
      car.style.transform = 'translateX(' + px + 'px)';
      skid.style.width = px + 'px';
      liveSpeed.textContent = fmt(v * 3.6, 1);
      livePos.textContent = fmt(x, 2);
      if(virtualElapsed < tStop){
        animId = requestAnimationFrame(frame);
      } else {
        liveSpeed.textContent = fmt(0,1);
        livePos.textContent = fmt(brakingDistance,2);
      }
    }
    animId = requestAnimationFrame(frame);
  }

  runBtn.addEventListener('click', runSimulation);

  validateMass();
  speedLabel.innerHTML = speedSlider.value + '<span> km/h</span>';
  drawLineChart(speedCanvas, [0], [0], { color: '#ffb703', yLabel: '속력 v (km/h)' });
  drawLineChart(positionCanvas, [0], [0], { color: '#4cc9c0', yLabel: '위치 x (m)' });
  refreshDistanceChart();
})();

</script>
</body>
</html>
