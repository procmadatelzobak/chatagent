# ChatAgent – vize a záznam rozhovoru

## Cíl projektu
ChatAgent je dvouvrstvý nástroj pro vývoj software. Vnější pracovník komunikuje s uživatelem, analyzuje jeho požadavky, ukládá kontext a zadává menší úkoly vnitřnímu pracovníkovi. Vnitřní pracovník je autonomní agent se přístupem k terminálu a GITu; vykonává zadané úkoly, dokud nejsou splněny, a zapisuje průběh i výsledky.

## Klíčové požadavky
- Backend: Python + FastAPI, SQLite, orkestrace úkolů, přístup k nástrojům (bash, git, souborové operace).
- Frontend: webové rozhraní v zeleném textu na černém pozadí ve stylu terminálu, s chatem, logy a přehledem projektů.
- LLM: primárně Google (Gemini) přes Chat Completions API, s možností rozšíření na další poskytovatele; musí být možnost omezit náklady (dle dolarů nebo tokenů).
- Embeddings: budou využity pro paměť a vyhledávání (uložení v SQLite).
- Paměť: per‑projektová, sdílená mezi oběma pracovníky; zápisky o průběhu práce a kontextu.
- Git: každý projekt jako repo pod `/home/<user>/chatagent/projects`, automatické commity.
- Přístup: běží na vlastním serveru s root právy (není izolováno), možnost pozdější self‑update a fallback na starší verzi.
- UI: možnost pauzovat, přehled tokenů/časů/nákladů, load/save projektů, monitoring vnitřního pracovníka.

## Záznam rozhovoru

### Uživatel
> Chci vytvořit následující aplikaci ChatAgent.
>
> Ty jsi v roli realizátora. Celé to budeš postupně dělat sám. Analýzu, návrh řešení, diskuzi, architekturu, vývoj, testování a opravy, nahrávání na GIT. Nahrávání na GIT a testování budeme řešit asi i agentem. Teď spolu začínáme rozhovor, co po tobě chci. Je to rozhovor, očekává se adekvátní účast obou stran. Ne nutně dlouhých zpráv, spíše jako v rozhovoru, ale jako realizátor se určitě potřebuješ na nějaké věci zeptat, abys věděl, jak to realizovat.  Znáš mě, trochu znám i já tebe. A nedávno jsme spolu právě tohle téma programovacího agenta řešili.
>
> ChatAgent je nástroj, program, sedící na linuxovém serveru, který je zcela jeho. Má tam administrátorská práva, je to virtuální počítač, a v rámci něj si může dělat, co chce. Má přístup k terminálu root.
>
> Slouží k vývoji aplikací. Vyvíjí aplikaci, synchronizuje s GITem, instaluje ji u sebe, testuje.
>
> Uživatel jej ovládá přes webové rozhraní. Po otevření vidí rozdělané projekty, které může otevřít a pokračovat v nich. Nebo může vytvořit nový projekt, smazat projekt.
>
> Když uživatel projekt otevře, bude komunikovat s LLM, kterému říkám vnější pracovník. Ten s uživatelem probírá, co uživatel vlastně chce, a případně dává pokyny dalšímu LLM, vnitřnímu pracovníkovi. To je vývojář, který aplikaci vyvíjí.
> Například s vnějším pracovníkem se uživatel domluví, co chce naprogramovat, prostřednictvím rozhovoru s vnějším pracovníkem. Vnější pracovník pak může předat pokyny vnitřnímu pracovníkovi, co má dělat.
> Práci mu musí dělit do menších dávek. Vnitřní pracovník pak pracuje samostatně jako agent, je to taky LLM, Má kompletní přístup do CLI, umí s gitem, vytvořit, editovat, mazat soubory. A dokud nesplní úkol, nebo se neobjeví problém, tak nepřestane pracovat. Jakmile úkol dokončí, předá o tom informaci vnějšímu pracovníkovi.
>
> Uživatel uvidí hlavně chat s vnějším pracovníkem, ale i výstup vnitřního pracovníka a další věci, které bude moci monitorovat. Bude moci pozastavit projekt, load/save projektů ze souboru, uvidí počty tokenů, strávený čas, za poslední zprávu, za poslední cyklus, za celý projekt, i kalkulaci nákladů přes API.
>
> LLM jsou připojené přes chat completions API. Primárně do OpenAI, ale i Google, na kterém to budeme testovat, deepseek a claude.
> Pro každý projekt tak musí existovat paměť. Taky vyžaduje rozsáhlou dokumentaci během postupného vývoje, commity na github, Ve vlastní paměti ale uchovává informace pro sebe o průběhu vývoje. Aby se mohl zpětně podívat, proč něco řešil konkrétním způsobem nebo na čem opakovaně selhává nebo naráží. Bude mít tedy nějakou sqlite, kam si bude ukládat zadání projektu a další informace. Jinak co bude možné, to bude uchovávat na githubu.
>
> Server, na kterém poběží, může být docela silný stroj. NVMe disky, desítky GB RAM a desítky vláken procesoru. Může tyto prostředky využívat. Nevím, jestli je možné použít v ChatCompletitions API vector storage, a zda by se to sem hodilo.
>
> Do paměti musí vidět oba LLM. Oba by si dělali i zápisky o postupu svojí práce.
>
> Je nutné, aby to šlo vytvořit pomocí dnešních možností. Režim agent není přes API dostupný, chci prostě LLM, které se tak ale bude chovat, byť jen v textové formě v CLI.
>
> Představuji si to tak, že uživatel bude probírat projekt s vnějším pracovníkem, Na té stránce uvidí chat, monitoring různých věcí, případně třeba i něco jako roadmapu, ale to zatím nebudeme implementovat. Vnější pracovník s uživatelem rozebere, co vlastně uživatel chce, jak to bude dělat, řešit. Bude si to ukládat, aby pro případ restartu mohl navázat, bude si v průběhu vytvářet do paměti různé potřebné dokumenty (popis projektu atd, ze kterých pak bude dělat do gitu readme, dokumentaci, bude podle něj vyvíjet atd). Rozdělí práci do fází, a ty bude předávat vnitřnímu pracovníkovi jako zadání práce, úkol k vyřešení. Ten se do nich pustí. Například "natři schody", vnitřní pracovník bude natírat, dokud nebude hotovo, a pak vrátí informaci o stavu vnitřnímu pracovníkovi.
> Vnější pracovník přitom stále může komunikovat s uživatelem a pracovat na dalších věcech.
>
> Má to sloužit k vývoji, testování, opravám softwaru s GITem pomocí LLM. Co nejvíce automatického, ale i responsivního.
>
> Musí to i nějak vypadat, očekávám hezký vzhled.
>
> Bude s tím dost práce, ale chtěl bych to vyvíjet postupně. Vlastně bych chtěl, abych to co nejdříve mohl vyvíjet v něm samotném, a tím ho rovnou vyzkoušet. Potřebujeme tedy začít od nějakého MVP.
>
> V minulém chatu jsi mi takový program skoro i vytvořil, ale zip soubory nešly stáhnout a chat se zasekl. Tak teď zahajuji nový, ale možná do té historie vidíš.

### Asistent
> Nazdar, Vojto. Rozumím: chceš “dvouvrstvého” programovacího agenta (vnější pracovník ↔ uživatel, vnitřní pracovník ↔ vývojář/agent s CLI), s pamětí, GITem, pěkným webem a multi-LLM přes chat completions. Pojďme to rozjet po částech.
>
> (…shrnutí MVP, technologie, otázky…)

### Uživatel
> enbeddings budeme chtit, souhlasim.
> Pokud jde nejak docilit toho, aby to delal v chat completititions chovanim agenta, pak nemusime loop ridit sami. Jde to?
> Musime setrit tokeny. Kazdy prompt vyzaduje velkou delku kontextu o projektu, pokynech atd, musime ji nejak setrit. Chovat se usporne.
> Na disku ho chci v /home/ jako uzivatele. At bezi snadno. Nechci /srv/
> Modelem chci zacit u Google, je do nejake miry zdarma. S moznosti vyberu jeho agentu. Potrebuji uzivatelskou moznost omezit cenu pomoci dolaru nebo poctu tokenu.
> Povolme root hned. Je to jeho virtual. Kdyztak se cely obnovi.
> Rozhrani chci ajtacke. Co nejvice uzitecne, treba zeleny text na cernem pozadi ve stylu starych terminalu, ale samozrejme s modernim ovladanim.
> Prijemne ovladatelne, podrobne.
>
> Nevim, kdy presne ho zacit vyvijet sama sebou. Jakmile by to melo byt mozne. Chci zkratit pocet kroku s tebou a prejit na chat s nim.
>
> A pak by mel idealne nekdy dostat i moznost aktualizace sebe , gitu, restart a idealne fallback na starsi verzi. Ale to neni treba mit hned.
>
> Potřebuji, abys do projektu zapsal, co je jeho cílem. Přesně definoval, jak má vypadat, prostě přenesl tam celý tenhle chat do githubu, aby bylo jasné, co se má programovat.
