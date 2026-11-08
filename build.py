# -*- coding: utf-8 -*-
"""
构建脚本：把字体与图片以 base64 注入，生成单页博客 index.html。
用法：python build.py
"""
import base64
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('ascii')

SIGNATURE = b64(os.path.join(ROOT, 'assets/signature.png'))
MC_LOGO   = b64(os.path.join(ROOT, 'assets/mc_logo.svg'))

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Felix Du · 个人博客</title>
<meta name="description" content="Felix Du 的个人博客">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%230A0A32'/%3E%3Ctext x='32' y='44' font-size='38' font-family='Georgia,serif' font-style='italic' font-weight='bold' fill='%23E8C890' text-anchor='middle'%3EF%3C/text%3E%3C/svg%3E">
<link rel="preload" href="assets/fonts/NotoSansSC-Regular.woff2" as="font" type="font/woff2" crossorigin>
<style>
/* ============ Fonts (独立文件，浏览器并行加载 + 缓存) ============ */
@font-face{font-family:'Noto Sans SC';src:url('assets/fonts/NotoSansSC-Regular.woff2') format('woff2');font-weight:400;font-style:normal;font-display:swap;}
@font-face{font-family:'Liberation Serif';src:url('assets/fonts/LiberationSerif-Regular.woff2') format('woff2');font-weight:400;font-style:normal;font-display:swap;}
@font-face{font-family:'Liberation Serif';src:url('assets/fonts/LiberationSerif-Bold.woff2') format('woff2');font-weight:700;font-style:normal;font-display:swap;}
@font-face{font-family:'Liberation Serif';src:url('assets/fonts/LiberationSerif-Italic.woff2') format('woff2');font-weight:400;font-style:italic;font-display:swap;}
@font-face{font-family:'Liberation Serif';src:url('assets/fonts/LiberationSerif-BoldItalic.woff2') format('woff2');font-weight:700;font-style:italic;font-display:swap;}

/* ============ Base ============ */
:root{
  --bg:#0A0A32;
  --name:#E8C890;
  --motto:#C8B8FF;
  --white:#FFFFFF;
  --accent:#5aa7ff;
  --accent-soft:rgba(90,167,255,0.14);
  --card:#12123f;
  --card-border:rgba(255,255,255,0.08);
  --text:#e8e8f4;
  --muted:#9a9ab8;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{
  background:var(--bg);
  color:var(--text);
  font-family:'Noto Sans SC','Source Han Sans SC','思源黑体','PingFang SC','Microsoft YaHei','Liberation Serif',sans-serif;
  line-height:1.7;
  min-height:100vh;
  overflow-x:hidden;
  -webkit-font-smoothing:antialiased;
}
/* 跟随鼠标的背景光晕 */
#bg-glow{
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(600px circle at var(--mx,50%) var(--my,30%), var(--accent-soft), transparent 65%);
  transition:background .3s ease;
}
.wrap{position:relative;z-index:1;max-width:760px;margin:0 auto;padding:0 20px 80px;}

/* ============ Language toggle ============ */
.lang-bar{display:flex;justify-content:flex-end;padding-top:16px;gap:8px;}
.lang-btn{
  background:transparent;border:1px solid var(--card-border);color:var(--muted);
  padding:5px 14px;border-radius:20px;cursor:pointer;font-size:13px;font-family:inherit;
  transition:all .25s ease;
}
.lang-btn.active,.lang-btn:hover{color:var(--white);border-color:var(--accent);background:var(--accent-soft);}

/* ============ Header ============ */
header{text-align:center;padding:44px 0 12px;}
.name{
  font-family:'Liberation Serif',serif;
  font-weight:700;font-style:italic;
  font-size:clamp(2.4rem,8vw,3.6rem);
  color:var(--name);
  letter-spacing:1px;
  animation:fadeDown .9s ease both;
}
.signature{
  display:block;margin:6px auto 2px;max-width:min(360px,70vw);height:auto;
  opacity:.95;animation:fadeDown .9s .15s ease both;
}
.motto{
  font-family:'Liberation Serif',serif;
  font-style:italic;font-weight:400;
  font-size:clamp(1.05rem,3.4vw,1.35rem);
  color:var(--motto);
  margin-top:4px;
  animation:fadeDown .9s .3s ease both;
}

/* ============ Sections ============ */
.profile{padding-top:8px;}
.section{
  margin-top:30px;padding:22px 22px;border-radius:16px;
  background:var(--card);border:1px solid var(--card-border);
  transition:transform .3s ease, box-shadow .3s ease, border-color .3s ease;
}
.section:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 12px 32px rgba(0,0,0,.35);}
.section h2{
  font-size:15px;text-transform:uppercase;letter-spacing:2px;
  color:var(--accent);margin-bottom:14px;font-weight:600;
}
.section h2::after{content:'';display:block;width:34px;height:2px;background:var(--accent);margin-top:6px;border-radius:2px;}
.body-text{font-size:15.5px;color:var(--text);}
.body-text .dim{color:var(--muted);}

/* contact links */
.contact-list{list-style:none;display:flex;flex-direction:column;gap:8px;}
.contact-list a{
  font-family:'Liberation Serif',serif;color:var(--white);
  text-decoration:none;font-size:15.5px;word-break:break-all;
  transition:color .25s ease, padding-left .25s ease;
}
.contact-list a:hover{color:var(--accent);padding-left:6px;}

/* birthday */
.birthday{font-family:'Liberation Serif',serif;font-size:1.35rem;color:var(--white);letter-spacing:1px;}

/* education timeline */
.edu-item{display:flex;gap:14px;margin-bottom:16px;}
.edu-item:last-child{margin-bottom:0;}
.edu-dot{flex:none;width:10px;height:10px;border-radius:50%;background:var(--accent);margin-top:8px;box-shadow:0 0 0 4px var(--accent-soft);}
.edu-time{flex:none;width:170px;color:var(--muted);font-size:13.5px;font-family:'Liberation Serif',serif;}
.edu-body{font-size:15px;}
.edu-body .school{font-weight:600;color:var(--white);}

/* minecraft */
.mc-box{display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center;}
.mc-logo-link{display:inline-block;transition:transform .35s ease;}
.mc-logo-link:hover{transform:scale(1.06) rotate(-1deg);}
.mc-logo-link img{width:min(300px,80vw);height:auto;display:block;}
.mc-name{font-size:1.1rem;color:var(--white);}
.mc-name b{color:var(--accent);}
.mc-skin{margin-top:4px;}
.mc-skin img{width:min(240px,70vw);height:auto;border-radius:10px;border:1px solid var(--card-border);image-rendering:pixelated;}

/* ============ Feed ============ */
.feed-head{margin-top:44px;text-align:center;}
.feed-title{font-family:'Liberation Serif',serif;font-size:1.7rem;color:var(--white);font-weight:700;font-style:italic;}
.feed-sub{color:var(--muted);font-size:13.5px;margin-top:2px;}
.toolbar{
  display:flex;flex-wrap:wrap;gap:10px;margin:20px 0 6px;align-items:center;
}
.search{
  flex:1 1 220px;min-width:160px;
  background:var(--card);border:1px solid var(--card-border);color:var(--text);
  padding:10px 16px;border-radius:24px;font-size:14.5px;font-family:inherit;outline:none;
  transition:border-color .25s ease, box-shadow .25s ease;
}
.search:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft);}
.date-select{
  background:var(--card);border:1px solid var(--card-border);color:var(--text);
  padding:10px 14px;border-radius:24px;font-size:14px;font-family:inherit;outline:none;cursor:pointer;
}
.date-select:focus{border-color:var(--accent);}

#feed{display:flex;flex-direction:column;gap:16px;margin-top:14px;}
.post{
  background:var(--card);border:1px solid var(--card-border);border-radius:16px;
  padding:20px 22px;opacity:0;transform:translateY(24px);
  transition:opacity .6s ease, transform .6s ease, border-color .3s ease, box-shadow .3s ease;
}
.post.visible{opacity:1;transform:translateY(0);}
.post:hover{border-color:var(--accent);box-shadow:0 10px 28px rgba(0,0,0,.3);}
.post-head{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap;}
.post-date{font-family:'Liberation Serif',serif;color:var(--accent);font-size:14px;letter-spacing:.5px;}
.post-time{color:var(--muted);font-size:12.5px;font-family:'Liberation Serif',serif;}
.post-content{
  font-size:15.5px;color:var(--text);white-space:pre-wrap;word-break:break-word;
}
/* 字体选择（硬编码样式） */
.post-content.font-sans{font-family:'Noto Sans SC','思源黑体','PingFang SC','Microsoft YaHei',sans-serif;}
.post-content.font-serif{font-family:'Liberation Serif','Noto Serif SC',serif;}
.post-content.font-mono{font-family:'Consolas','Courier New',monospace;}
.post-content.font-kai{font-family:'KaiTi','STKaiti','Kaiti SC','楷体','Noto Sans SC',serif;}
.post-content.font-cute{font-family:'Noto Sans SC','PingFang SC','Microsoft YaHei',sans-serif;font-weight:600;}
.post-media{display:flex;flex-direction:column;gap:12px;margin-top:14px;}
.post-media img{width:100%;border-radius:10px;border:1px solid var(--card-border);cursor:zoom-in;transition:transform .3s ease;}
.post-media img:hover{transform:scale(1.02);}
.post-media video{width:100%;border-radius:10px;background:#000;outline:none;}
.post-media audio{width:100%;outline:none;}
.multi-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;}
.multi-grid img{width:100%;height:160px;object-fit:cover;border-radius:10px;cursor:zoom-in;}

#load-more{display:flex;justify-content:center;margin-top:24px;}
#load-more button{
  background:transparent;border:1px solid var(--card-border);color:var(--muted);
  padding:10px 30px;border-radius:24px;cursor:pointer;font-size:14px;font-family:inherit;
  transition:all .3s ease;
}
#load-more button:hover{color:var(--white);border-color:var(--accent);background:var(--accent-soft);}
#feed-empty{text-align:center;color:var(--muted);padding:50px 0;display:none;}

footer{text-align:center;color:var(--muted);font-size:12.5px;margin-top:60px;font-family:'Liberation Serif',serif;}

/* lightbox */
#lightbox{position:fixed;inset:0;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;z-index:99;cursor:zoom-out;}
#lightbox img{max-width:92vw;max-height:90vh;border-radius:8px;}

/* ============ Animations ============ */
@keyframes fadeDown{from{opacity:0;transform:translateY(-24px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeUp{from{opacity:0;transform:translateY(26px);}to{opacity:1;transform:translateY(0);}}

/* 滚动出现 */
.reveal{opacity:0;transform:translateY(26px);transition:opacity .7s ease, transform .7s ease;}
.reveal.visible{opacity:1;transform:translateY(0);}

@media (max-width:560px){
  .edu-item{flex-direction:column;gap:6px;}
  .edu-time{width:auto;}
  .wrap{padding:0 16px 60px;}
}
</style>
</head>
<body>
<div id="bg-glow"></div>

<div class="wrap">
  <div class="lang-bar">
    <button class="lang-btn active" data-lang="zh">中文</button>
    <button class="lang-btn" data-lang="en">English</button>
  </div>

  <header>
    <div class="name">Felix Du</div>
    <img class="signature" src="data:image/png;base64,__SIGNATURE__" alt="signature">
    <div class="motto">All that glitters is not gold.</div>
  </header>

  <main class="profile">
    <section class="section reveal">
      <h2 data-i18n="origin">名字来源</h2>
      <p class="body-text" data-i18n="originText">我的中文名叫杜悦菲。Felix 在拉丁语中意为"幸福的"，与"悦"相对应；Felix 的中文译名是"菲利克斯"，与"菲"相对应。</p>
    </section>

    <section class="section reveal">
      <h2 data-i18n="birthday">生日</h2>
      <div class="birthday" data-i18n="birthdayText">2012年8月10日</div>
    </section>

    <section class="section reveal">
      <h2 data-i18n="contact">联系我</h2>
      <ul class="contact-list">
        <li><a href="mailto:duyuefei2023@outlook.com">duyuefei2023@outlook.com</a></li>
        <li><a href="mailto:duyuefei2026@outlook.com">duyuefei2026@outlook.com</a></li>
        <li><a href="mailto:felixdu2012@outlook.com">felixdu2012@outlook.com</a></li>
        <li><a href="mailto:1807969637@qq.com">1807969637@qq.com</a></li>
      </ul>
    </section>

    <section class="section reveal">
      <h2 data-i18n="edu">受教育经历</h2>
      <div class="edu-item">
        <span class="edu-dot"></span>
        <span class="edu-time">2018.9.1 – 2024.7.1</span>
        <div class="edu-body"><span class="school" data-i18n="edu1s">小学 · 西安市特立实验小学</span></div>
      </div>
      <div class="edu-item">
        <span class="edu-dot"></span>
        <span class="edu-time">2024.9.1 – <span data-i18n="now">至今</span></span>
        <div class="edu-body"><span class="school" data-i18n="edu2s">初中 · 西安市曲江第一学校（铁一曲江）</span></div>
      </div>
    </section>

    <section class="section reveal">
      <h2 data-i18n="game">最喜欢的游戏</h2>
      <div class="mc-box">
        <a class="mc-logo-link" href="https://www.minecraft.net" target="_blank" rel="noopener">
          <img src="data:image/svg+xml;base64,__MC_LOGO__" alt="Minecraft">
        </a>
        <div class="mc-name"><span data-i18n="gameName">游戏名</span>：<b>DYF2012</b></div>
        <div class="mc-skin"><img src="image2.png" loading="lazy" alt="Minecraft skin"></div>
      </div>
    </section>

    <div class="feed-head">
      <div class="feed-title" data-i18n="feedTitle">我的动态</div>
      <div class="feed-sub" data-i18n="feedSub">下拉加载更多 · 支持日期筛选与关键词搜索</div>
    </div>

    <div class="toolbar">
      <input class="search" id="search" type="text" placeholder="搜索关键词… / Search…">
      <select class="date-select" id="dateFilter">
        <option value="all" data-i18n="allDate">全部日期</option>
      </select>
    </div>

    <div id="feed"></div>
    <div id="feed-empty" data-i18n="noPost">暂无内容</div>
    <div id="load-more" style="display:none;"><button id="loadMoreBtn" data-i18n="loadMore">加载更多</button></div>
  </main>

  <footer>© <span id="year"></span> Felix Du · Powered by GitHub Pages</footer>
</div>

<div id="lightbox"><img id="lightbox-img" src="" alt=""></div>

<script>
(function(){
  'use strict';

  /* ============ 主题色（按当天日期算法生成） ============ */
  function themeColorByDate(date){
    var s = date.getFullYear() + '-' + String(date.getMonth()+1).padStart(2,'0') + '-' + String(date.getDate()).padStart(2,'0');
    var h = 0;
    for (var i=0;i<s.length;i++){ h = (h * 131 + s.charCodeAt(i)) >>> 0; }
    var hue = h % 360;
    return 'hsl(' + hue + ', 72%, 62%)';
  }
  function applyTheme(){
    var c = themeColorByDate(new Date());
    var soft = c.replace(')', ', 0.15)').replace('hsl', 'hsla');
    document.documentElement.style.setProperty('--accent', c);
    document.documentElement.style.setProperty('--accent-soft', soft);
  }
  applyTheme();
  document.getElementById('year').textContent = new Date().getFullYear();

  /* ============ 鼠标移动背景光晕 ============ */
  var glow = document.getElementById('bg-glow');
  document.addEventListener('mousemove', function(e){
    glow.style.setProperty('--mx', e.clientX + 'px');
    glow.style.setProperty('--my', e.clientY + 'px');
  });

  /* ============ 中英双语切换 ============ */
  var I18N = {
    origin:{zh:'名字来源',en:'Origin of My Name'},
    originText:{zh:'我的中文名叫杜悦菲。Felix 在拉丁语中意为"幸福的"，与"悦"相对应；Felix 的中文译名是"菲利克斯"，与"菲"相对应。',en:'My Chinese name is Du Yuefei. "Felix" means "happy / fortunate" in Latin, corresponding to "悦" (Yuè). The Chinese transliteration of Felix is "菲利克斯" (Fēilìkèsī), corresponding to "菲" (Fēi).'},
    birthday:{zh:'生日',en:'Birthday'},
    birthdayText:{zh:'2012年8月10日',en:'August 10, 2012'},
    contact:{zh:'联系我',en:'Contact Me'},
    edu:{zh:'受教育经历',en:'Education'},
    edu1s:{zh:'小学 · 西安市特立实验小学',en:'Primary School · Xi\'an Teli Experimental Primary School'},
    edu2s:{zh:'初中 · 西安市曲江第一学校（铁一曲江）',en:'Middle School · Xi\'an Qujiang No.1 School (Tieyi Qujiang)'},
    now:{zh:'至今',en:'Present'},
    game:{zh:'最喜欢的游戏',en:'Favorite Game'},
    gameName:{zh:'游戏名',en:'Game name'},
    feedTitle:{zh:'我的动态',en:'My Moments'},
    feedSub:{zh:'下拉加载更多 · 支持日期筛选与关键词搜索',en:'Scroll for more · Filter by date & search'},
    allDate:{zh:'全部日期',en:'All dates'},
    noPost:{zh:'暂无内容',en:'No posts yet'},
    loadMore:{zh:'加载更多',en:'Load more'}
  };
  var currentLang = 'zh';
  var langBtns = document.querySelectorAll('.lang-btn');
  langBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      currentLang = btn.getAttribute('data-lang');
      langBtns.forEach(function(b){ b.classList.toggle('active', b===btn); });
      document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';
      applyI18n();
      renderPosts();  // re-render feed labels
    });
  });
  function t(key){ return I18N[key] ? I18N[key][currentLang] : key; }
  function applyI18n(){
    document.querySelectorAll('[data-i18n]').forEach(function(el){
      el.textContent = t(el.getAttribute('data-i18n'));
    });
  }
  applyI18n();

  /* ============ 滚动出现动画 ============ */
  var revealObs = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if (en.isIntersecting){ en.target.classList.add('visible'); revealObs.unobserve(en.target); }
    });
  }, {threshold:0.08});
  document.querySelectorAll('.reveal').forEach(function(el){ revealObs.observe(el); });

  /* ============ 帖子数据 ============ */
  var allPosts = [];
  var shownCount = 0;
  var PAGE = 5;
  var feedEl = document.getElementById('feed');
  var loadMoreWrap = document.getElementById('load-more');
  var emptyEl = document.getElementById('feed-empty');

  function postFontClass(f){ 
    var map = {sans:'font-sans',serif:'font-serif',mono:'font-mono',kai:'font-kai',cute:'font-cute'};
    return map[f] || 'font-sans';
  }
  function esc(s){ return String(s).replace(/[&<>"']/g, function(m){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]; }); }
  function mediaHTML(media){
    if (!media || !media.length) return '';
    var images = media.filter(function(m){ return m.type === 'image'; });
    var rest = media.filter(function(m){ return m.type !== 'image'; });
    var html = '';
    if (images.length > 1){
      html += '<div class="multi-grid">' + images.map(function(m){
        return '<img src="' + esc(m.src) + '" loading="lazy" alt="">';
      }).join('') + '</div>';
    } else if (images.length === 1){
      html += '<img src="' + esc(images[0].src) + '" loading="lazy" alt="">';
    }
    rest.forEach(function(m){
      if (m.type === 'video') html += '<video src="' + esc(m.src) + '" controls preload="metadata"></video>';
      else if (m.type === 'audio') html += '<audio src="' + esc(m.src) + '" controls preload="metadata"></audio>';
    });
    return html ? '<div class="post-media">' + html + '</div>' : '';
  }
  function renderPost(p){
    var d = new Date(p.date + 'T00:00:00');
    var dateStr = isNaN(d) ? p.date : (d.getFullYear() + '/' + String(d.getMonth()+1).padStart(2,'0') + '/' + String(d.getDate()).padStart(2,'0'));
    var el = document.createElement('article');
    el.className = 'post';
    el.innerHTML = 
      '<div class="post-head"><span class="post-date">' + esc(dateStr) + '</span><span class="post-time">' + esc(p.time || '') + '</span></div>' +
      '<div class="post-content ' + postFontClass(p.font) + '">' + esc(p.content) + '</div>' +
      mediaHTML(p.media);
    feedEl.appendChild(el);
    // reveal
    requestAnimationFrame(function(){ el.classList.add('visible'); });
  }
  function applyFilters(){
    var kw = document.getElementById('search').value.trim().toLowerCase();
    var df = document.getElementById('dateFilter').value;
    var list = allPosts.filter(function(p){
      if (df !== 'all' && p.date !== df) return false;
      if (kw){
        var hay = (p.content || '').toLowerCase();
        var mediaNames = (p.media || []).map(function(m){ return m.src; }).join(' ').toLowerCase();
        if (hay.indexOf(kw) === -1 && mediaNames.indexOf(kw) === -1) return false;
      }
      return true;
    });
    feedEl.innerHTML = '';
    shownCount = 0;
    loadMoreWrap.style.display = list.length > PAGE ? 'flex' : 'none';
    emptyEl.style.display = list.length === 0 ? 'block' : 'none';
    for (var i=0;i<Math.min(PAGE, list.length);i++){ renderPost(list[i]); shownCount++; }
    return list;
  }
  var filtered = [];
  function renderPosts(){
    filtered = applyFilters();
  }
  document.getElementById('search').addEventListener('input', renderPosts);
  document.getElementById('dateFilter').addEventListener('change', renderPosts);
  document.getElementById('loadMoreBtn').addEventListener('click', function(){
    for (var i=shownCount; i<Math.min(shownCount+PAGE, filtered.length); i++){ renderPost(filtered[i]); }
    shownCount = Math.min(shownCount+PAGE, filtered.length);
    if (shownCount >= filtered.length) loadMoreWrap.style.display = 'none';
  });

  /* ============ 图片灯箱 ============ */
  var lightbox = document.getElementById('lightbox');
  var lightboxImg = document.getElementById('lightbox-img');
  feedEl.addEventListener('click', function(e){
    if (e.target.tagName === 'IMG'){ lightboxImg.src = e.target.src; lightbox.style.display = 'flex'; }
  });
  lightbox.addEventListener('click', function(){ lightbox.style.display = 'none'; });

  /* ============ 加载 posts.json ============ */
  fetch('posts.json', {cache:'no-store'})
    .then(function(r){ if (!r.ok) throw new Error('HTTP '+r.status); return r.json(); })
    .then(function(data){
      allPosts = (data.posts || []).sort(function(a,b){ return (b.date + ' ' + (b.time||'')).localeCompare(a.date + ' ' + (a.time||'')); });
      // 填充日期筛选
      var dates = {};
      allPosts.forEach(function(p){ dates[p.date] = true; });
      var sel = document.getElementById('dateFilter');
      Object.keys(dates).sort().reverse().forEach(function(d){
        var opt = document.createElement('option');
        opt.value = d; opt.textContent = d;
        sel.appendChild(opt);
      });
      renderPosts();
    })
    .catch(function(err){
      console.error('load posts.json failed:', err);
      emptyEl.textContent = currentLang === 'zh' ? '加载内容失败' : 'Failed to load posts';
      emptyEl.style.display = 'block';
    });
})();
</script>
</body>
</html>
"""

html = HTML
html = html.replace('__SIGNATURE__', SIGNATURE)
html = html.replace('__MC_LOGO__', MC_LOGO)

out = os.path.join(ROOT, 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print('generated', out, '%.1f MB' % (os.path.getsize(out) / 1024 / 1024))
