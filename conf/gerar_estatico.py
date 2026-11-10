"""
Gera index.html (dashboard estático) a partir da planilha da Matriz de Expansão.
Uso:  python gerar_estatico.py [planilha.xlsx] [--chave SUA_CHAVE_GOOGLE_MAPS]
Sem --chave o mapa usa OpenStreetMap; com a chave, usa o Google Maps.
Requer: pip install pandas openpyxl
Não embute telefone nem nome de representante (a página pode ficar pública).
"""
import argparse, json, re, unicodedata
from datetime import date, datetime
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("planilha", nargs="?", default="MATRIZ_EXPANSAO_PRONTA_LOOKER.xlsx")
ap.add_argument("--chave", default="")
a = ap.parse_args()
NI = "Não informado"

MODELO = r"""<!doctype html>
<html lang="pt-BR" translate="no"><head><meta charset="utf-8"><meta name="google" content="notranslate">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>TETO PE – Matriz de Expansão</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
:root{--bg:#fff;--fg:#1c1c1c;--card:#f1f5f4}@media(prefers-color-scheme:dark){:root{--bg:#171717;--fg:#eee;--card:#262626}}
body{margin:auto;padding:16px;font:15px system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:1200px}
h1{font-size:1.5rem}select,button{padding:6px 10px;margin:0 6px 6px 0;background:var(--card);color:var(--fg);border:1px solid #8884;border-radius:6px}
nav button{font-size:1rem}nav button.on{border-color:#1976d2;font-weight:700}.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:10px 0}
.c{background:var(--card);padding:10px 14px;border-radius:8px}.c small{display:block;opacity:.7}.c b{font-size:1.6rem}
.g2{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:10px}#gm,#om{height:560px}.t{overflow-x:auto}
table{border-collapse:collapse;width:100%}td,th{padding:5px 8px;border-bottom:1px solid #8884;text-align:left;font-size:.9rem}a{color:#1976d2}
small,footer{opacity:.7}footer{margin:16px 0;font-size:.85rem}
</style></head><body>
<h1>Matriz de Expansão – TETO Pernambuco</h1>
<div id="f"></div><small id="nota"></small><div id="kpi" class="g"></div>
<nav><button data-t="viz" class="on">📊 Visão geral</button><button data-t="mapa">🗺️ Mapa</button><button data-t="tab">📋 Tabela</button><button data-t="pend">⚠️ Pendências</button></nav>
<section id="viz"><div class="g2"><div id="c1"></div><div id="c2"></div><div id="c3"></div>
<div><select id="eixo"><option>Década de formação</option><option>Ano de formação</option><option>Demanda construtiva</option></select><div id="c4"></div></div></div></section>
<section id="mapa" style="display:none"><select id="por"><option value="status">Colorir por status</option><option value="cat">Colorir por categoria</option></select>
<small id="sem"></small><div id="gm"></div><div id="om"></div><div id="leg"></div><div id="det">Clique em um ponto do mapa para ver os detalhes.</div></section>
<section id="tab" style="display:none"><div class="t" id="tb"></div></section>
<section id="pend" style="display:none"><small>Itens a corrigir na base (aba PENDENCIAS da planilha).</small><div class="t" id="pd"></div></section>
<footer>Dados atualizados em __GERADO__. Só aparecem no mapa as comunidades com coordenadas.</footer>
<script>
const D=__DATA__,P=__PEND__,KEY="__CHAVE__",NI="Não informado",$=i=>document.getElementById(i),
F=[["mun","Município"],["status","Status padronizado"],["cat","Categoria"],["lid","Liderança"],["mv","Origem MV"],["fund","Situação fundiária"],["risco","Risco ambiental"],["dem","Demanda construtiva"]],
sel={},COR={"Já trabalhamos":"#2e7d32","Já visitamos":"#1976d2","Não visitamos":"#e65100",[NI]:"#9e9e9e"},
PAL=["#1976d2","#2e7d32","#e65100","#8e24aa","#00838f","#c62828","#6d4c41","#9e9e9e"],CATS=[...new Set(D.map(d=>d.cat))].sort();
const cor=(d,p)=>p==="status"?COR[d.status]||"#888":PAL[CATS.indexOf(d.cat)%PAL.length],vz=[];
let aba="viz",M,MK=[],IW,pronto=!KEY;
F.forEach(([k,t])=>{const o=[...new Set(D.map(d=>d[k]))].sort();if(o.length<2&&o[0]===NI){vz.push(t);return}
 const s=document.createElement("select");s.innerHTML=`<option value="">${t}: todos</option>`+o.map(v=>`<option>${v}</option>`).join("");
 s.onchange=()=>{sel[k]=s.value;draw()};$("f").append(s)});
if(vz.length)$("nota").textContent="Ainda sem dados na planilha: "+vz.join(", ")+".";
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{aba=b.dataset.t;
 document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x===b));
 ["viz","mapa","tab","pend"].forEach(t=>$(t).style.display=t===aba?"block":"none");draw()});
$("eixo").onchange=$("por").onchange=()=>draw();
const cnt=(a,k)=>Object.entries(a.reduce((m,d)=>(m[d[k]]=(m[d[k]]||0)+1,m),{})),
info=d=>`<b>${d.nome}</b><br>${d.mun} · ${d.status}<br>Categoria: ${d.cat} · Liderança: ${d.lid}<br>Famílias: ${d.fam??"—"}<br>
<a target="_blank" href="https://www.google.com/maps?q=${d.lat},${d.lon}">Google Maps</a>`+(d.earth?` · <a target="_blank" href="${d.earth}">Google Earth</a>`:""),
tabela=(h,l)=>`<table><tr>${h.map(x=>`<th>${x}</th>`).join("")}</tr>${l.map(r=>`<tr>${r.map(x=>`<td>${x}</td>`).join("")}</tr>`).join("")}</table>`;
if(KEY){window.gok=()=>{pronto=true;draw()};const s=document.createElement("script");
 s.src=`https://maps.googleapis.com/maps/api/js?key=${KEY}&callback=gok`;s.async=true;document.head.append(s)}
function draw(){
 const r=D.filter(d=>F.every(([k])=>!sel[k]||d[k]===sel[k])),id=r.filter(d=>d.idade!=null);
 $("kpi").innerHTML=[["Comunidades",r.length],["Famílias mapeadas",r.reduce((s,d)=>s+(d.fam||0),0).toLocaleString("pt-BR")],
 ["Com enquete aplicada",r.length?Math.round(100*r.filter(d=>d.enq).length/r.length)+"%":"—"],
 ["Idade média (anos)",id.length?(id.reduce((s,d)=>s+d.idade,0)/id.length).toFixed(1):"—"]].map(([t,v])=>`<div class="c"><small>${t}</small><b>${v}</b></div>`).join("");
 const L={paper_bgcolor:"rgba(0,0,0,0)",plot_bgcolor:"rgba(0,0,0,0)",font:{color:getComputedStyle(document.body).color},margin:{t:40,l:50,r:10,b:40}};
 if(aba==="viz"){
  const m=cnt(r,"mun").sort((a,b)=>b[1]-a[1]),pie=(i,t,k,cf)=>{const e=cnt(r,k);
   Plotly.react(i,[{type:"pie",hole:.5,labels:e.map(x=>x[0]),values:e.map(x=>x[1]),marker:cf?{colors:e.map(x=>cf(x[0]))}:{}}],{...L,title:t})};
  Plotly.react("c1",[{type:"bar",x:m.map(e=>e[0]),y:m.map(e=>e[1]),text:m.map(e=>e[1]),marker:{color:"#1976d2"}}],{...L,title:"Comunidades por município"});
  pie("c2","Status padronizado","status",x=>COR[x]||"#888");pie("c3","Situação fundiária","fund",null);
  const ev=$("eixo").value,e=ev==="Demanda construtiva"?cnt(r.filter(d=>d.dem!==NI),"dem"):
   cnt(r.filter(d=>d.ano).map(d=>({p:ev[0]==="D"?Math.floor(d.ano/10)*10+"s":String(d.ano)})),"p").sort();
  if(!e.length){Plotly.purge("c4");$("c4").textContent="Sem dados preenchidos para este gráfico."}
  else Plotly.react("c4",[{type:"bar",orientation:"h",y:e.map(x=>x[0]),x:e.map(x=>x[1]),text:e.map(x=>x[1]),marker:{color:"#1976d2"}}],
   {...L,title:"Comunidades por "+ev.toLowerCase(),yaxis:{type:"category",autorange:"reversed"},xaxis:{dtick:1}})}
 if(aba==="mapa"){
  const g=r.filter(d=>d.lat!=null),p=$("por").value,ks=[...new Set(g.map(d=>p==="status"?d.status:d.cat))];
  $("sem").textContent=` ${g.length} de ${r.length} comunidades filtradas têm coordenadas.`;
  $("leg").innerHTML=ks.map(k=>`<span style="color:${cor(g.find(d=>(p==="status"?d.status:d.cat)===k),p)}">●</span> ${k} &nbsp;`).join("");
  $("gm").style.display=KEY?"block":"none";$("om").style.display=KEY?"none":"block";
  if(KEY&&pronto&&window.google){
   if(!M){M=new google.maps.Map($("gm"),{center:{lat:-8.05,lng:-34.9},zoom:10});IW=new google.maps.InfoWindow()}
   MK.forEach(m=>m.setMap(null));MK=[];const b=new google.maps.LatLngBounds();
   g.forEach(d=>{const q={lat:d.lat,lng:d.lon};b.extend(q);const m=new google.maps.Marker({position:q,map:M,title:d.nome,
    icon:{path:google.maps.SymbolPath.CIRCLE,scale:Math.max(7,Math.min(16,Math.sqrt(d.fam||60)*.9)),fillColor:cor(d,p),fillOpacity:.85,strokeColor:"#fff",strokeWeight:1}});
    m.addListener("click",()=>{IW.setContent(info(d));IW.open(M,m)});MK.push(m)});
   if(g.length){M.fitBounds(b,40);google.maps.event.addListenerOnce(M,"idle",()=>{if(M.getZoom()>15)M.setZoom(15)})}}
  if(!KEY){
   let c={lat:-8.05,lon:-34.9},z=9;
   if(g.length){const la=g.map(d=>d.lat),lo=g.map(d=>d.lon),x=Math.max(Math.max(...la)-Math.min(...la),.01)*1.4,y=Math.max(Math.max(...lo)-Math.min(...lo),.01)*1.4;
    c={lat:(Math.max(...la)+Math.min(...la))/2,lon:(Math.max(...lo)+Math.min(...lo))/2};z=Math.min(Math.log2(560*360/(512*x)),Math.log2(($("om").clientWidth||900)*360/(512*y)),12.5)}
   Plotly.react("om",ks.map(k=>{const a=g.filter(d=>(p==="status"?d.status:d.cat)===k);return{type:"scattermapbox",mode:"markers",name:k,lat:a.map(d=>d.lat),lon:a.map(d=>d.lon),
    text:a.map(d=>`<b>${d.nome}</b><br>${d.mun}<br>Famílias: ${d.fam??"—"}`),hoverinfo:"text",customdata:a.map(d=>d.nome),
    marker:{size:a.map(d=>Math.max(10,Math.min(26,Math.sqrt(d.fam||60)*1.6))),color:cor(a[0],p)}}}),
    {...L,mapbox:{style:"open-street-map",center:c,zoom:z},margin:{t:0,l:0,r:0,b:0},height:560,legend:{orientation:"h"}},{responsive:true});
   if(!$("om").dataset.on){$("om").dataset.on=1;$("om").on("plotly_click",e=>{$("det").innerHTML=info(D.find(x=>x.nome===e.points[0].customdata))})}}}
 if(aba==="tab")$("tb").innerHTML=tabela(["Comunidade","Município","Status","Categoria","Liderança","Famílias","Enquete","Origem MV","Mapa"],
  r.map(d=>[d.nome,d.mun,d.status,d.cat,d.lid,d.fam??"—",d.enq?"Sim":"Não",d.mv,d.lat!=null?`<a target="_blank" href="https://www.google.com/maps?q=${d.lat},${d.lon}">abrir</a>`:"—"]));
 if(aba==="pend")$("pd").innerHTML=tabela(P.cols,P.rows);
}
draw();
</script></body></html>
"""


def vazio(v):
    return v is None or (not isinstance(v, str) and pd.isna(v)) or str(v).strip() in ("", "-")


def txt(v, pad=NI):
    return pad if vazio(v) else re.sub(r"\.0$", "", re.sub(r"\s+", " ", str(v)).strip())


def nz(v):
    try:
        return None if vazio(v) else float(v)
    except ValueError:
        return None


def chave(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s).strip().lower()


def coords(r):
    m = re.match(r"^\s*(-?\d+(?:[.,]\d+)?)\s*[,;]\s*(-?\d+(?:[.,]\d+)?)\s*$", str(r.get("COORDENADAS_MANUAL")))
    if m:
        return float(m[1].replace(",", ".")), float(m[2].replace(",", "."))
    la, lo = nz(r.get("LATITUDE_LINK")), nz(r.get("LONGITUDE_LINK"))
    if la is not None and lo is not None:
        return la, lo
    m = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", str(r.get("LINK_EARTH")))
    return (float(m[1]), float(m[2])) if m else (None, None)


df = pd.read_excel(a.planilha, sheet_name="BASE_LOOKER")
rows, vistos = [], set()
for _, r in df.iterrows():
    nome = txt(r.get("NOME_COMUNIDADE"), "")
    if not nome or chave(nome) in vistos:
        continue
    vistos.add(chave(nome))
    mv = txt(r.get("ORIGEM_MV"), "") or ("MV 2026" if r.get("Aba_Origem") == "MV2604" else "Fora do MV")
    cat = txt(r.get("CATEGORIA"))
    cat = "Revisar (valor 2026)" if re.fullmatch(r"\d{4}", cat) else cat
    ano, idade = nz(r.get("ANO_FORMACAO")), nz(r.get("IDADE_ANOS"))
    if idade is None and ano:
        idade = date.today().year - ano
    la, lo = coords(r)
    link = r.get("LINK_EARTH")
    rows.append(dict(
        nome=nome, mun=txt(r.get("MUNICIPIO")), status=txt(r.get("STATUS_PADRONIZADO"), "Não visitamos"), cat=cat,
        lid={"sim": "Sim", "nao": "Não"}.get(chave(r.get("LIDERANCA_PADRONIZADA")), NI), mv=mv,
        fund=txt(r.get("SITUACAO_FUNDIARIA")), risco=txt(r.get("RISCO_AMBIENTAL")), dem=txt(r.get("DEMANDA_CONSTRUTIVA")),
        fam=nz(r.get("N_FAMILIAS")), enq=int(nz(r.get("ENQUETE_FLAG")) or 0), ano=ano, idade=idade, lat=la, lon=lo,
        earth=link if isinstance(link, str) and link.startswith("http") else None))

try:
    pd_ = pd.read_excel(a.planilha, sheet_name="PENDENCIAS")
    pend = dict(cols=[str(c) for c in pd_.columns], rows=[[txt(v, "") for v in l] for l in pd_.itertuples(index=False)])
except Exception:
    pend = dict(cols=["Aviso"], rows=[["Aba PENDENCIAS não encontrada."]])

js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = (MODELO.replace("__DATA__", js(rows)).replace("__PEND__", js(pend)).replace("__CHAVE__", a.chave)
        .replace("__GERADO__", datetime.now().strftime("%d/%m/%Y")))
open("index.html", "w", encoding="utf-8").write(html)
print(f"index.html gerado: {len(rows)} comunidades, {sum(d['lat'] is not None for d in rows)} no mapa, "
      f"mapa {'Google' if a.chave else 'OpenStreetMap (sem --chave)'}")
