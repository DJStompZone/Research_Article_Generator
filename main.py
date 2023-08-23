from metaphor_python import Metaphor
import openai
import requests
from bs4 import BeautifulSoup
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.metrics import jaccard_distance
from citeproc.source.json import CiteProcJSON
from citeproc import CitationStylesStyle, CitationStylesBibliography
import networkx as nx
client = Metaphor(api_key="3e5db288-bfc5-49be-aab7-3a18d97dc67d")
openai.api_key = "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"

news = [
    "bbc.com", "nytimes.com", "washingtonpost.com", "reuters.com", "apnews.com",
    "theguardian.com", "wsj.com", "bloomberg.com", "economist.com", "cnn.com",
    "aljazeera.com", "npr.org", "pbs.org", "latimes.com", "time.com",
    "usatoday.com", "abcnews.go.com", "independent.co.uk",
    "ft.com", "huffpost.com", "chicagotribune.com", "thehill.com",
    "politico.com", "bloombergquint.com", "hindustantimes.com",
    "dw.com", "cbc.ca", "japantimes.co.jp", "france24.com",
    "reuters.co.uk", "telegraph.co.uk", "thetimes.co.uk", "thestar.com",
    "msnbc.com", "salon.com", "theconversation.com", "theintercept.com", "vox.com",
    "slate.com", "thedailystar.net", "africanews.com", "scmp.com", "thenation.com",
    "theglobeandmail.com", "abc.net.au", "sfgate.com", "thenewamerican.com",
    "nydailynews.com", "dailymail.co.uk", "usnews.com", "usnews.nbcnews.com",
    "nzherald.co.nz", "detroitnews.com", "boston.com", "insideedition.com",
    "cbsnews.com", "cnbc.com", "cfr.org", "telesurtv.net", "thelocal.de",
    "politifact.com", "theguardian.ng", "scotsman.com",
    "irishexaminer.com", "thehindu.com", "timesofindia.indiatimes.com", "cbcnews.ca",
    "aajtak.in", "lefigaro.fr", "rt.com", "alarabiya.net", "haaretz.com",
    "thejc.com", "arstechnica.com", "wnyc.org", "news.ycombinator.com", "theonion.com",
    "thewire.in", "publicintegrity.org", "voanews.com", "chalkbeat.org",
    "thedailybeast.com"
]

schooling = [
    "ed.gov", "unesco.org", "educationworld.com", "chronicle.com", "edutopia.org", "nea.org",
    "edweek.org", "economist.com", "ted.com", "education.com", "npr.org", "educationnews.org",
    "theatlantic.com", "nea.today", "edsource.org", "hechingerreport.org", "edutopia.org",
    "campusreform.org", "educationdive.com", "usnews.com", "educationnext.org", "nafsa.org",
    "educationviews.org", "learningscientists.org", "teachforamerica.org", "kqed.org",
    "aera.net", "edleadersnetwork.org", "edtrust.org", "edfunders.org", "aacc.nche.edu",
    "nafme.org", "teach.org", "ascd.org", "iste.org", "nctm.org",
    "nais.org", "education.unicefusa.org", "education.ucsb.edu", "teachercast.net",
    "hepg.org", "eab.com", "educationnext.org", "teachertube.com"
]

science = [
    "sciencemag.org", "nature.com", "pubs.acs.org", "pnas.org", "newscientist.com",
    "nationalgeographic.com", "popsci.com", "phys.org", "sciencedaily.com", "scientificamerican.com",
    "smithsonianmag.com", "nasa.gov", "esa.int", "jpl.nasa.gov", "sciam.com",
    "natureworldnews.com", "eurekalert.org", "space.com", "wired.com", "cnet.com",
    "pbs.org", "discovermagazine.com", "the-scientist.com", "aps.org", "chemistryworld.com",
    "cen.acs.org", "chemistryviews.org", "rsc.org", "biologynews.net", "ncbi.nlm.nih.gov",
    "genome.gov", "cell.com", "journals.plos.org", "pnas.org", "physiology.org", "sciencedirect.com",
    "ieee.org", "neurosciencenews.com", "sciencenews.org", "livescience.com", "futurism.com",
    "npr.org", "quantamagazine.org", "spaceandbeyondbox.com", "sciencemuseum.org.uk", "ucmp.berkeley.edu",
    "serc.carleton.edu", "sciencenode.org", "biologydictionary.net", "chemguide.co.uk",
    "pbslearningmedia.org", "physicstoday.scitation.org", "biologycorner.com", "acs.org", "nsta.org",
    "physicsworld.com", "biology-online.org", "nasa.gov", "spaceplace.nasa.gov", "biologynews.net",
    "pbs.org", "understandingscience.org", "nature.com", "popsci.com", "biologicaldiversity.org",
    "chemeddl.org", "lpi.usra.edu", "sciencemadesimple.com", "phy-astr.gsu.edu", "serc.carleton.edu",
    "scitable.com", "apsnet.org", "iflscience.com", "newatlas.com", "scienceline.org", "phys.org",
    "colorado.edu", "biology-pages.info", "sciencenotes.org", "nytimes.com", "chemistry.about.com",
    "worldofmolecules.com", "nsta.org", "sciencenewsforstudents.org", "iop.org", "nps.gov", "explorable.com",
    "hyperphysics.phy-astr.gsu.edu", "climate.nasa.gov", "periodicvideos.com", "scq.ubc.ca", "helix.northwestern.edu",
    "aps.org", "education.jlab.org", "pdb101.rcsb.org", "the-scientist.com"
]

technology = [
    "wired.com", "techcrunch.com", "arstechnica.com", "thenextweb.com", "cnet.com",
    "engadget.com", "mashable.com", "theverge.com", "gizmodo.com", "zdnet.com",
    "venturebeat.com", "slashdot.org", "techradar.com", "makeuseof.com", "gigaom.com",
    "readwrite.com", "androidauthority.com", "androidcentral.com", "macrumors.com", "9to5mac.com",
    "9to5google.com", "9to5linux.com", "9to5toys.com", "androidpolice.com", "appleinsider.com",
    "tomshardware.com", "digitaltrends.com", "pcworld.com", "theinquirer.net"]


health = [
    "nih.gov", "who.int", "cdc.gov", "mayoclinic.org", "webmd.com",
    "medlineplus.gov", "harvard.edu", "mayo.edu", "nejm.org", "jamanetwork.com",
    "healthline.com", "sciencedaily.com", "medicalnewstoday.com", "bmj.com",
    "ncbi.nlm.nih.gov", "ahajournals.org", "hopkinsmedicine.org", "ahrq.gov",
    "verywellhealth.com", "drugs.com", "clevelandclinic.org", "emedicinehealth.com", "medscape.com",
    "stanfordhealthcare.org", "uofmhealth.org", "ucsfhealth.org", "ama-assn.org", "pennmedicine.org",
    "cdc.gov"
]


history = [
    "history.com", "britannica.com", "metmuseum.org", "smithsonianmag.com", "historytoday.com",
    "britishmuseum.org", "natgeokids.com", "britishheritage.com", "livescience.com", "ancient.eu",
    "historyextra.com", "worldhistory.org", "historyworld.net", "pbs.org", "newyorker.com",
    "amnh.org", "theguardian.com", "mentalfloss.com", "theatlantic.com", "ancient-origins.net",
    "historynet.com", "nps.gov", "historyforkids.net", "en.wikipedia.org", "britishcouncil.org",
    "loc.gov", "usc.edu", "crystalinks.com", "besthistorysites.net",
    "metmuseum.org", "worldhistory.org", "historyplace.com", "historyguide.org", "thenile.ca", 
    "historyexplorer.si.edu", "britannica.com", "ancient.eu", "british-history.ac.uk", "historymuseum.ca",
    "journals.plos.org", "bl.uk", "historyextra.com", "fsmitha.com",
    "thoughtco.com", "historians.org", "history.com",
    "historians.org", "khanacademy.org", "historyextra.com", "pbs.org",
    "ancient.eu", "historymuseum.ky.gov", "time.com", "brilliant.org",
    "history.howstuffworks.com", "news.nationalgeographic.com", "thegreatcoursesplus.com", "historyplace.com",
    "kidskonnect.com", "spartacus-educational.com", "thehistorypress.co.uk", "thebritishhistorypodcast.com",
    "historyhit.com", "historicalnovels.info", "archives.gov", "historyextra.com", "neok12.com",
    "ancestry.com", "historyforkids.net", "travel.nationalgeographic.com", "timeline.com", "slaveryimages.org",
    "nehistory.org", "blackpast.org", "pbs.org", "pbs.org", "pbs.org",
    "historymuseum.ky.gov", "museumoflondon.org.uk", "historyteachersattic.com", "berlinerfestspiele.de", "shmoop.com",
    "ushistory.org", "worldhistory.mrdonn.org", "timemaps.com", "exploringafrica.matrix.msu.edu", "britishpathe.com",
    "ancient-origins.net", "primaryhomeworkhelp.co.uk", "thirteen.org", "worldhistory.mrdonn.org",
    "penn.museum", "britishempire.co.uk", "aasd.k12.wi.us", "merriam-webster.com",
    "odysseetheater.org", "icp.org", "www2.census.gov", "historicalnovelsociety.org", "nj.gov"
]

educational = [
    "khanacademy.org", "coursera.org", "edx.org", "udemy.com", "mit.edu",
    "codecademy.com", "udacity.com", "k12.com", "pbslearningmedia.org", "scholastic.com",
    "coolmath.com", "funbrain.com", "brainpop.com", "nationalgeographickids.com", "abcya.com",
    "starfall.com", "mathplayground.com", "readwritethink.org", "storybird.com", "storyjumper.com",
    "carnegielibrary.org", "crashcourse.org", "ted.com", "britannica.com", "howstuffworks.com",
    "nasa.gov", "exploratorium.edu", "historyforkids.net", "kids.nationalgeographic.com", "sheppardsoftware.com",
    "timeforkids.com", "kids.britannica.com", "magicblox.com", "newsela.com", "duolingo.com",
    "factmonster.com", "grammarly.com", "read.gov", "npr.org", "nps.gov",
    "scholar.google.com", "ask.com", "mentalfloss.com", "jstor.org", "wolframalpha.com",
    "sparknotes.com", "cliffsnotes.com", "quizlet.com", "wordreference.com", "merriam-webster.com",
    "dictionary.cambridge.org", "oxfordlearnersdictionaries.com", "thesaurus.com", "poetryfoundation.org", "readpoetry.com",
    "artforkidshub.com", "pbskids.org", "funology.com", "discoverykids.com", "imaginationlibrary.com",
    "seussville.com", "create.kahoot.it", "learninggamesforkids.com", "kidsfront.com",
    "edu.gcfglobal.org", "youngzine.org", "tinkercad.com", "scratch.mit.edu", "edheads.org",
    "kids.mysterynet.com", "storylineonline.net", "toytheater.com", "kids.niehs.nih.gov",
    "coolmath4kids.com", "howtosmile.org", "earthday.org", "kidsactivitiesblog.com", "teacher.scholastic.com",
    "makebeliefscomix.com", "educationworld.com", "starwarsintheclassroom.com", "bbc.co.uk", "abc.net.au",
    "teachertube.com", "pebblego.com", "kids.usa.gov", "kids.gov", "library.thinkquest.org",
    "gamestarmechanic.com", "highlightskids.com", "natgeokids.com", "virtualnerd.com", "discoverexplorelearn.com",
    "kidinfo.com", "learningplanet.com", "homeadvisor.com", "teachinghistory.org", "readingrockets.org",
    "thekidshouldseethis.com", "cyberkidzgames.com", "abcmouse.com", "learning.games", "flocabulary.com",
    "typingclub.com", "epicreads.com", "abc.net.au", "education.jlab.org", "mocomi.com",
    "switchzoo.com", "cyberchase.mom", "eduweb.com"
]
computerscience = [
    "stackoverflow.com", "github.com", "w3schools.com", "tutorialspoint.com", "geeksforgeeks.org",
    "developer.mozilla.org", "machinelearningmastery.com", "kaggle.com", "fast.ai", "datasciencecentral.com",
    "arxiv.org", "towardsdatascience.com", "colab.research.google.com", "ai.google", "openai.com",
    "tensorflow.org", "pytorch.org", "scikit-learn.org", "keras.io", "docs.microsoft.com",
    "dev.to", "codecademy.com", "freeCodeCamp.org", "hackerrank.com", "leetcode.com",
    "hackerearth.com", "codeforces.com", "projecteuler.net", "ros.org", "udacity.com",
    "coursera.org", "edx.org", "linkedin.com", "pluralsight.com", "egghead.io",
    "udemy.com", "techcrunch.com", "theverge.com", "wired.com", "techradar.com",
    "venturebeat.com", "cnet.com", "engadget.com", "arstechnica.com", "slashdot.org",
    "techspot.com", "mashable.com", "androidauthority.com", "macrumors.com", "futurism.com",
    "androidpolice.com", "appleinsider.com", "9to5mac.com", "9to5google.com", "androidcentral.com",
    "techdirt.com", "extremetech.com", "android.com", "developers.google", "developer.apple.com",
    "opensource.com", "gitlab.com", "stackexchange.com", "hackernews.com", "freecodecamp.org",
    "reddit.com", "neuralnetworksanddeeplearning.com", "ml-cheatsheet.readthedocs.io", "peterbloem.nl", "explainable.ai",
    "lilianweng.github.io", "r2rt.com", "distill.pub", "karpathy.github.io", "colah.github.io",
    "ai.googleblog.com", "sebastianraschka.com", "turing.ml", "datacamp.com", "huggingface.co",
    "paperswithcode.com", "mlflow.org", "pycaret.org", "deeplearning.ai", "fast.ai"
]
environment = [
    "nrdc.org", "wwf.org", "greenpeace.org", "sierraclub.org", "nature.org",
    "defenders.org", "conservation.org", "earthjustice.org", "wildlife.org", "eia-international.org",
    "edf.org", "worldwildlife.org", "rainforestfoundation.org", "iucn.org", "oceana.org",
    "bioneers.org", "ecowatch.com", "earthday.org", "theoceancleanup.com", "savetheelephants.org",
    "c40.org", "rainforesttrust.org", "panda.org", "globalwildlife.org", "seashepherd.org",
    "janeGoodall.org", "oneearth.org", "greenbeltmovement.org", "birds.cornell.edu", "environmentaldefense.org",
    "ucsusa.org", "mangroveactionproject.org", "wcs.org", "wri.org", "cspinet.org",
    "whales.org", "awf.org", "wildlifedirect.org", "coral.org", "oceanconservancy.org",
    "treehugger.com", "motherearthnews.com", "earthisland.org", "nationalgeographic.com", "ecology.com",
    "conservationevidence.com", "earthworksaction.org", "fws.gov", "oceancrusaders"]

religion = [
"britannica.com", "plato.stanford.edu", "iep.utm.edu", "philpapers.org", "religiousstudiesproject.com",
"patheos.com", "beliefnet.com", "religionnews.com", "catholicnewsagency.com", "chabad.org",
"buddhanet.net", "hinduwebsite.com", "islamreligion.com", "sikhiwiki.org", "jewishvirtuallibrary.org",
"biblegateway.com", "quran.com", "dhammatalks.org", "sacred-texts.com", "academia.edu",
"jstor.org", "oxfordbiblicalstudies.com", "academic.oup.com", "standardebooks.org",
"worldcat.org", "religion-online.org", "religiouseducation.net", "anglicannews.org", "episcopalchurch.org",
"bhagavad-gita.org", "biblehub.com", "bhagavad-gita.us", "theravada-dhamma.org", "vatican.va",
"yogajournal.com", "easternphilosophy.co.uk", "philosophybasics.com", "vedabase.io", "internetencyclopediaofphilosophy.com"

]


economics = [
"economist.com", "wsj.com", "ft.com", "bloomberg.com", "cnbc.com",
"forbes.com", "businessweek.com", "investopedia.com", "marketwatch.com", "seekingalpha.com",
"hbr.org", "entrepreneur.com", "inc.com", "fastcompany.com", "thestreet.com",
"barrons.com", "reuters.com", "cnbc.com", "econlib.org", "worldbank.org",
"weforum.org", "imf.org", "wto.org", "fed.gov", "bls.gov",
"bea.gov", "ny.frb.org", "stlouisfed.org", "jpmorganchase.com", "goldmansachs.com",
"morganstanley.com", "bankofamerica.com", "wellsfargo.com", "citi.com", "barclays.com",
"blackrock.com", "vanguard.com", "fidelity.com", "ubs.com", "pimco.com",
"nytimes.com", "theguardian.com", "businessinsider.com", "fool.com"

]


government = [
"whitehouse.gov", "senate.gov", "house.gov", "congress.gov", "supremecourt.gov",
"usa.gov", "fbi.gov", "cia.gov", "nsa.gov", "justice.gov",
"state.gov", "treasury.gov", "defense.gov", "homelandsecurity.gov", "uscourts.gov",
"census.gov", "irs.gov", "epa.gov", "sba.gov", "fdic.gov",
"uspto.gov", "ssa.gov", "nasa.gov", "archives.gov", "libraryofcongress.gov",
"un.org", "wto.org", "imf.org", "worldbank.org", "who.int",
"europa.eu", "nato.int", "commonwealth.org", "npr.org", "c-span.org",
"bbc.com", "reuters.com", "nytimes.com", "theguardian.com", "politico.com",
"washingtonpost.com", "huffpost.com", "cnn.com", "nbcnews.com", "abcnews.go.com",
"pbs.org", "cbsnews.com", "foxnews.com", "apnews.com", "usatoday.com",
"newsweek.com", "thehill.com", "rollcall.com", "nationaljournal.com", "realclearpolitics.com",
"fivethirtyeight.com", "theatlantic.com", "time.com", "slate.com", "theintercept.com",
"vox.com", "motherjones.com", "washingtonexaminer.com", "dailykos.com", "mediamatters.org",
"drudgereport.com", "breitbart.com", "infowars.com", "thinkprogress.org", "theamericanconservative.com",
"heritage.org", "brookings.edu", "rand.org", "cfr.org", "pewresearch.org",
"gallup.com", "factcheck.org", "opensecrets.org", "govtrack.us", "ballotpedia.org",
"ontheissues.org", "votesmart.org", "propublica.org", "sunlightfoundation.com", "electoral-vote.com",
"538.com", "cookpolitical.com", "politifact.com"
]

law = [
    "supremecourt.gov", "law.cornell.edu", "findlaw.com", "justia.com", "abaforlawstudents.com",
"usnews.com", "jurist.org", "law360.com", "lawyers.com", "nolo.com",
"theguardian.com", "reuters.com", "nytimes.com", "washingtonpost.com", "cnn.com",
"bbc.com", "usatoday.com", "apnews.com", "nbcnews.com", "abcnews.go.com",
"cbsnews.com", "c-span.org", "uscourts.gov", "justice.gov", "fdic.gov",
"irs.gov", "fbi.gov", "dea.gov", "atf.gov", "usmarshals.gov",
"ojp.gov", "bjs.gov", "ncjrs.gov", "bop.gov", "ada.gov",
"cafc.uscourts.gov", "ca9.uscourts.gov", "ca2.uscourts.gov", "ca1.uscourts.gov", "dcd.uscourts.gov",
"nysd.uscourts.gov", "scotusblog.com", "oyez.org"

]

nonprofits = [
"charitynavigator.org", "guidestar.org", "nonprofitquarterly.org", "philanthropy.com", "nonprofitaf.com",
"ssir.org", "npengage.com", "npjournal.org", "nonprofithub.org", "bloomerang.co",
"idealist.org", "volunteermatch.org", "donorschoose.org", "globalgiving.org", "charitywater.org",
"savethechildren.org", "oxfam.org", "amnesty.org", "unicef.org", "humanrightsfirst.org",
"redcross.org", "care.org", "doctorswithoutborders.org", "worldwildlife.org", "greenpeace.org",
"aclu.org", "naacp.org", "plannedparenthood.org", "amnestyusa.org", "rainn.org",
"350.org", "sierraclub.org", "nrdc.org", "earthjustice.org", "nwf.org",
"eff.org", "transparency.org", "openrightsgroup.org", "hrw.org", "freepress.net",
"actionaid.org", "surfrider.org", "change.org", "avaaz.org", "sumofus.org",
"care2.com", "moveon.org", "witness.org", "demos.org", "fairvote.org",
"everyaction.com", "tides.org", "civicus.org", "resist.org", "colorofchange.org",
"publiccitizen.org", "commoncause.org", "thetransitionnetwork.org", "charityvillage.com", "grassrootsfund.org",
"allianceofhope.org", "worldvolunteerweb.org", "nonprofitcenters.org", "volunteeringaustralia.org", "philanthropyroundtable.org",
"asiapacificphilanthropy.org", "philanthropyforum.org", "givingforum.org", "ecofriendlynonprofits.org", "nonprofitlawblog.com",
"foundationcenter.org", "boardsource.org", "nonprofitfinancefund.org", "nonprofitmarketingguide.com", "nonprofitmarketingblog.com",
"nonprofitchronicles.com", "blueavocado.org", "bolderadvocacy.org", "probono.net", "nonprofitrisk.org",
"tsne.org"

]

countries = [
    "cia.gov", "bbc.com", "theguardian.com", "reuters.com", "nytimes.com",
"dw.com", "aljazeera.com", "time.com", "cnn.com", "usatoday.com",
"apnews.com", "nbcnews.com", "abcnews.go.com", "cbsnews.com", "rt.com",
"economist.com", "foreignpolicy.com", "worldpoliticsreview.com", "un.org", "oneworld.net",
"worldbank.org", "imf.org", "weforum.org", "globalpolicy.org", "transparency.org",
"hrw.org", "amnesty.org", "icrc.org", "heritage.org", "transatlanticrelations.org",
"pewresearch.org", "cfr.org", "chathamhouse.org", "brookings.edu", "wilsoncenter.org",
"carnegieendowment.org", "isi.org", "oxfam.org", "unicef.org", "who.int",
"unesco.org", "iucn.org", "worldwildlife.org", "greenpeace.org", "culturalpolicies.net",
"britannica.com", "lonelyplanet.com", "heritage.org", "worldatlas.com", "nationsonline.org",
"nationsencyclopedia.com", "infoplease.com", "atlasobscura.com", "theculturetrip.com", "everyculture.com",
"worldmusiccentral.org", "worldhistory.org", "washingtonpost.com", "aljazeera.com", "abc.net.au",
"euobserver.com", "thelocal.eu", "latinnews.com", "africa.upenn.edu", "allAfrica.com"

]

geography = [
"geographic.org", "geographycat.com", "worldatlas.com", "nationsonline.org", "nationalgeographic.com",
"britannica.com", "geographyrealm.com", "geographynotes.com", "geographyfieldwork.com", "geographyeducation.org",
"geography.howstuffworks.com", "en.wikipedia.org", "geography.about.com", "universetoday.com", "geography.name",
"geography4kids.com", "geographybase.com", "coolgeography.co.uk", "geographypods.com", "onlinegeography.com",
"geographyas.info", "world-geography-games.com", "mrreid.org", "gcu.edu", "theconversation.com",
"geography-news.blogspot.com", "geosociety.org", "geographyalltheway.com", "worldgeography.org", "geography-site.co.uk",
"sgs.org.uk", "geographyworldonline.com", "teacherlink.ed.usu.edu", "geographygeek.com", "geography.tki.org.nz",
"geomaps.geology.iastate.edu", "atlasobscura.com", "worldmapper.org", "maphill.com", "mapsofworld.com",
"mapquest.com", "openstreetmap.org", "google.com", "bing.com", "geology.com",
"earth.google.com", "nasa.gov", "usgs.gov", "maps.nationalgeographic.com", "mapsofindia.com",
"infoplease.com", "maproom.org", "geographicguide.com", "lizardpoint.com", "citypopulation.de",
"natgeomaps.com", "lib.utexas.edu/maps", "freeworldmaps.net", "statisticalatlas.com", "cartography.org"

]


entertainment = [
"foodnetwork.com", "myrecipes.com", "eater.com", "thespruceeats.com", "foodandwine.com", "tasteofhome.com", "spoonforkbacon.com",
"twopeasandtheirpod.com", "thepioneerwoman.com", "inspiredtaste.net", "skinnytaste.com", "halfbakedharvest.com", "minimalistbaker.com",
"ambitiouskitchen.com", "cookieandkate.com", "foodiecrush.com", "foodbeast.com", "deliciouslyella.com", "ohsheglows.com",
"loveandlemons.com", "smittenkitchen.com", "pinchofyum.com", "budgetbytes.com", "thugkitchen.com", "cupofjo.com",
"eonline.com", "variety.com", "hollywoodreporter.com", "ew.com", "deadline.com", "rottentomatoes.com", "imdb.com",
"boxofficemojo.com", "vulture.com", "collider.com", "screenrant.com", "entertainmentweekly.com", "metacritic.com", "fandango.com",
"ign.com", "sports.yahoo.com", "espn.com", "bleacherreport.com", "cbssports.com", "sportsillustrated.cnn.com", "nba.com",
"nfl.com", "mlb.com", "nhl.com", "fifa.com", "olympics.com", "ussoccer.com", "pga.com", "nascar.com", "ufc.com", "mlssoccer.com",
"tennis.com", "wwe.com", "wnba.com", "boxing.com", "cricket.com", "rugbyworldcup.com", "wimbledon.com", "usopen.org", "masters.com",
"nba.com", "nhl.com", "mlb.com", "nfl.com", "atptour.com", "fiba.basketball", "olympics.com", "uclabruins.com", "euroleague.net",
"usaswimming.org", "olympicchannel.com", "baseball-reference.com", "socceramerica.com", "worldfootball.net", "bbref.com",
"pro-football-reference.com", "basketball-reference.com", "hockey-reference.com", "sports-reference.com", "whoscored.com",
"flashscore.com", "sportsnet.ca", "nbcsports.com", "sbnation.com"

]

engineering = [
    "asce.org", "engineering.com", "engineersjournal.ie", "engineeringtoolbox.com", "engineeringnews.co.za", "engineerjobs.com",
"discovere.org", "engineering.columbia.edu", "engineering.mit.edu", "engineering.cambridge.edu", "engineering.nyu.edu",
"engineering.harvard.edu", "engineering.berkeley.edu", "engineering.stanford.edu", "engineering.ucla.edu", "engineering.uiowa.edu",
"engineering.purdue.edu", "engineering.illinois.edu", "engineering.cornell.edu", "engineering.umich.edu", "engineering.osu.edu",
"engineering.tamu.edu", "engineering.umass.edu", "engineering.ufl.edu", "engineering.umn.edu", "engineering.colorado.edu",
"engineering.washington.edu", "engineering.rutgers.edu", "engineering.uwaterloo.ca", "engineering.sjsu.edu", "engineering.unl.edu",
"engineering.tulane.edu", "engineering.uark.edu", "engineering.uconn.edu", "engineering.buffalo.edu", "engineering.missouri.edu",
"engineering.pitt.edu", "engineering.utah.edu", "engineering.mtu.edu", "engineering.uco.edu", "engineering.wpi.edu",
"engineering.oregonstate.edu", "engineering.uab.edu", "engineering.fiu.edu", "engineering.udel.edu", "engineering.uta.edu",
"engineering.binghamton.edu", "engineering.rowan.edu", "engineering.byu.edu", "engineering.ksu.edu", "engineering.nd.edu",
"engineering.neu.edu", "engineering.ttu.edu", "engineering.uncc.edu", "engineering.unr.edu", "engineering.tntech.edu",
"engineering.miami.edu", "engineering.utdallas.edu", "engineering.uh.edu", "engineering.temple.edu", "engineering.uic.edu",
"engineering.njit.edu", "engineering.wwu.edu", "engineering.unm.edu", "engineering.nmsu.edu", "engineering.calpoly.edu",
"engineering.sdsu.edu", "engineering.umbc.edu", "engineering.cmu.edu", "engineering.mines.edu", "engineering.umaine.edu",
"engineering.arizona.edu", "engineering.wisc.edu", "engineering.uakron.edu", "asce.org", "nspe.org", "ieee.org", "aia.org",
"sae.org", "iie.org", "asee.org", "asme.org", "imeche.org", "ice.org.uk", "ieeexplore.ieee.org", "sciencedirect.com", "nature.com",
"cambridge.org", "onlinelibrary.wiley.com", "acs.org", "mdpi.com", "springer.com", "journals.sagepub.com", "journals.elsevier.com",
"journals.springer.com"

]

arts = [
    "arts.gov", "artnews.com", "artforum.com", "tate.org.uk", "moma.org", "louvre.fr", "guggenheim.org", "ngv.vic.gov.au", "britishmuseum.org",
"getty.edu", "artinstitutechicago.org", "rijksmuseum.nl", "museoreinasofia.es", "vam.ac.uk", "sfmoma.org", "architecturelab.net",
"archdaily.com", "architecturaldigest.com", "dezeen.com", "archinect.com", "architizer.com", "archisoup.com", "architectsjournal.co.uk",
"architectmagazine.com", "designboom.com", "musiciansfriend.com", "billboard.com", "rollingstone.com", "pitchfork.com", "npr.org",
"grammy.com", "music.apple.com", "spotify.com", "soundcloud.com", "pandora.com", "architecture.com", "architecture.org",
"architectureanddesign.com.au", "architecturelab.net", "architectmagazine.com", "archinect.com", "archdaily.com", "dezeen.com",
"architizer.com", "architectsjournal.co.uk", "danceusa.org", "dancemagazine.com", "pointemagazine.com", "dancemedia.com", "danceadvantage.net",
"dance-teacher.com", "dancespirit.com", "ballet.org.uk", "abt.org", "nycballet.com", "alvinailey.org", "russianballet.org", "dance.com",
"artsy.net", "artnet.com", "saatchiart.com", "artstation.com", "deviantart.com", "artspace.com", "ugallery.com", "1stdibs.com",
"invaluable.com", "blouinartinfo.com", "music.apple.com", "spotify.com", "soundcloud.com", "pandora.com", "last.fm", "music.yandex.com",
"tidal.com", "deezer.com", "amazon.com", "bbc.co.uk", "classical-music.com", "classicalarchives.com", "pitchfork.com", "rollingstone.com",
"billboard.com"

]

admissions = [
"collegeboard.org", "commonapp.org", "ucop.edu", "applyweb.com", "coalitionforcollegeaccess.org",
"nacacnet.org", "colleges.niche.com", "petersons.com", "collegeconfidential.com", "cappex.com",
"usnews.com", "princetonreview.com", "fastweb.com", "collegedata.com", "unigo.com",
"educationcorner.com", "collegexpress.com", "bigfuture.collegeboard.org", "collegeview.com", "niche.com",
"collegescorecard.ed.gov", "commonblackcollegeapp.com", "youvisit.com", "careerbuilder.com", "indeed.com",
"glassdoor.com", "linkedin.com", "monster.com", "simplyhired.com", "usajobs.gov",
"dice.com", "ziprecruiter.com", "careerjet.com", "snagajob.com", "neuvoo.com",
"craigslist.org", "job.com", "sciencecareers.sciencemag.org", "universityaffairs.ca", "jobs.ac.uk",
"chronicle.com", "theguardian.com", "nature.com", "timeshighereducation.com", "google.com"

]

psychology = [
"apa.org", "psychologytoday.com", "psychcentral.com", "verywellmind.com", "nami.org",
"nimh.nih.gov", "mind.org.uk", "psychologicalscience.org", "psycom.net", "talkspace.com",
"betterhelp.com", "goodtherapy.org", "psychiatry.org", "socialpsychology.org", "positivelypsychology.com",
"psychologynetwork.com", "allpsychologycareers.com", "psychologyinfo.com", "psychforums.com", "therapyroute.com",
"simplypsychology.org", "medicalnewstoday.com", "medicalxpress.com", "theguardian.com", "as.nyu.edu",
"thoughtco.com", "aamft.org", "aacp.com", "wellness.com", "mindbodygreen.com",
"wellnessmama.com", "verywellfit.com", "thewellnessway.com", "womenshealthmag.com", "wellness.columbia.edu",
"wellness.ucr.edu", "nhs.uk", "positivelypositive.com", "mindful.org"

]

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(list_to_check):
        if value == item_to_find:
            indices.append(idx)
    return indices

def find_similar_text(target_text, website_text):
    matches = difflib.get_close_matches(target_text, website_text, n=1, cutoff=0.4)
    if matches:
        return matches[0]
    else:
        return None

def extract3(prompt):
    prompt_template = """You will be given a topic, and must deterimine what topic it fits best under: news, schooling, educational, nonprofit, law, politics, economics, health, science, admissions, psychological, arts, engineering, entertainment, computer science, history, countries, geography, technology, or religion. Only output the category name, uncapitalized, no other surrounding text.\nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def extract4(prompt):
    prompt_template = """You will be given an input sentence, followed by two other sentences, all of which are separated by commas, which came after the input sentence in the order given. Please give a new form of the input sentence that is general knowledge and would not have to be cited, but also works well in the context. Only output the new form of the input sentence, nothing else.\nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def extract5(prompt):
    prompt_template = """You will be given an input sentence, followed by two other sentences, all of which separated by commas, which came before the input sentence in the order given. Please give a new form of the input sentence that is general knowledge and would not have to be cited, but also works well in the context. Only output the new form of the input sentence, nothing else.\nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def extract6(prompt):
    prompt_template = """You will be given an input sentence, followed by two other sentences, all of which separated by commas. The first of these two other sentences came before the input sentence, while the second of these two others sentences came after the input sentence. Please give a new form of the input sentence that is general knowledge and would not have to be cited, but also works well in the context. Only output the new form of the input sentence, nothing else.\nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def extract2(prompt):
    prompt_template = """You will be given two statements separated by a comma, and must determine which statement is most broad. If it is the first statement, output the number 1, if it is the second statement, output the number 2. \nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def finaloutput(prompt):
    prompt_template = """You will be given an article that is poorly formatted. Split it by the specified subsections (as indicated by numbers and a hyphen various subsections). \nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def generate(prompt):
    prompt_template = """You will be given a url as an input, and you will need to output an APA citation from that. Only output the citation, nothing else. If you are unable to access the external website directly to generate a citation, return the input url and nothing else, no error message, nothing talking about your capabilities, just the unchanged input url.\nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    return result

def extract(prompt):
    category=extract3(prompt)
    if(category=="news"):
        intended_domain=news
    elif(category=="schooling"):
        intended_domain=schooling
    elif(category=="arts"):
        intended_domain=arts
    elif(category=="science"):
        intended_domain=science
    elif(category=="law"):
        intended_domain=law
    elif(category=="politics"):
        intended_domain=government
    elif(category=="computer science"):
        intended_domain=computerscience
    elif(category=="geography"):
        intended_domain=geography
    elif(category=="countries"):
        intended_domain=countries
    elif(category=="nonprofit"):
        intended_domain=nonprofits
    elif(category=="economics"):
        intended_domain=economics
    elif(category=="educational"):
        intended_domain=educational
    elif(category=="psychological"):
        intended_domain=psychology
    elif(category=="engineering"):
        intended_domain=engineering
    elif(category=="health"):
        intended_domain=health
    elif(category=="science"):
        intended_domain=science
    elif(category=="admissions"):
        intended_domain=admissions
    elif(category=="entertainment"):
        intended_domain=entertainment
    elif(category=="technology"):
        intended_domain=technology
    elif(category=="religion"):
        intended_domain=religion
    elif(category=="history"):
        intended_domain=history

    prompt_template = """You will be given a topic, and must write an article based on it. It should be split into at least three different subsections, and each subsection should have three to four paragraphs. For each subsection, label it with a number, followed by a hyphen, not a period. \nInput: {}:""".format(prompt)
    request = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt_template}]
    )
    result = request['choices'][0]['message']['content']
    #print(result)
    messages=result.split(".")
    finalmessages=messages[:-1]
    total_num=len(finalmessages)
    dag = nx.DiGraph()
    for i in range (0, total_num):
        dag.add_node(str(i),label=str(i))
    for i in range(0,total_num-1):
        for j in range (i+1,total_num):
            statement_1=finalmessages[i]
            statement_2=finalmessages[j]
            lemmatizer = WordNetLemmatizer()
            tokens_1 = [lemmatizer.lemmatize(token) for token in word_tokenize(statement_1.lower())]
            tokens_2 = [lemmatizer.lemmatize(token) for token in word_tokenize(statement_2.lower())]
            jaccard_dist = jaccard_distance(set(tokens_1), set(tokens_2))
            jaccard_threshold = 0.75
            if jaccard_dist < jaccard_threshold:
                implication=extract2(statement_1+","+statement_2)
                if(implication=="1"):
                    dag.add_edge(str(i),str(j))
                else:
                    dag.add_edge(str(j),str(i))
    sentences_to_be_cited=[node for node in dag.nodes() if dag.in_degree(node) == 0]
    num_sentences=len(sentences_to_be_cited)
    citations=[]
    counter=1
    for k in range(0, num_sentences):
        index=int(sentences_to_be_cited[k])
        necessaryquery=finalmessages[index]
        response=client.search(necessaryquery+", "+prompt,num_results=5,include_domains=intended_domain)
        websites_num=len(response.results)
        for n in range(websites_num):
            link=response.results[n].url
            #print(response.results[n].url)
            website=requests.get(link)
            if(website.status_code==200):
                soup=BeautifulSoup(website.content, "html.parser")
                website_text = [text for text in soup.stripped_strings]
                similar_text = find_similar_text(necessaryquery, website_text)
                if similar_text:
                    #print(similar_text)
                    #print(f"Similar text found.")
                    citations.append(link)
                    finalmessages[index]+="["+str(counter)+"]"
                    counter+=1
                    break
                elif(n==websites_num-1):
                    #print("No similar text found.")
                    citations.append("Not found")
    if(citations.count("Not found")!=0):
        uncited=find_indices(citations, "Not found")
        for i in uncited:
            myindex=int(sentences_to_be_cited[i])
            themessage=finalmessages[myindex]
            if(myindex==0):
                second_sentence=finalmessages[1]
                third_sentence=finalmessages[2]
                finalmessages[myindex]=extract4(str(themessage)+","+str(second_sentence)+","+str(third_sentence))
            elif(myindex==len(finalmessages)-1):
                second_sentence=finalmessages[len(finalmessages)-2]
                first_sentence=finalmessages[len(finalmessages)-3]
                finalmessages[myindex]=extract5(str(themessage)+","+str(first_sentence)+","+second_sentence)
            else:
                before=finalmessages[myindex-1]
                after=finalmessages[myindex+1]
                finalmessages[myindex]=extract6(str(themessage)+","+str(before)+","+str(after))
    bibliography=""
    count=1
    duplicate_prevention=[]
    for k in range(0,len(citations)):
        if(citations[k]!="Not found"):
            if(citations[k] not in duplicate_prevention):
                APA_citation=generate(citations[k])
                #response = requests.get(citations[k])
                #html_content = response.content
                #soup = BeautifulSoup(html_content, "html.parser")
                #title = soup.title.get_text()
                #author = soup.find("meta", {"name": "author"})["content"] if soup.find("meta", {"name": "author"}) else None
                #publication_date = soup.find("meta", {"name": "publication_date"})["content"] if soup.find("meta", {"name": "publication_date"}) else "n.d."
                #citation_data = [
                   # {
                      #  "id": "item-1",
                     #   "type": "webpage",
                    #    "title": title,
                   #     "author": [{"family": author}] if author else None,
                  #      "issued": {"raw": publication_date},
                 #       "URL": citations[k],
                #    }
                #]

                #style = CitationStylesStyle("apa-7")

                #bib_source = CiteProcJSON(citation_data)

               # bibliography = CitationStylesBibliography(style, bib_source, validate=False)

                #citations = bibliography.bibliography()
                bibliography+=str(count)+"."+str(APA_citation)+"\n"
                count+=1
                duplicate_prevention.append(citations[k])
    response=""
    for i in range(len(finalmessages)):
        response+=finalmessages[i]+"."+" "

    output=finaloutput(response)
    print(output)
    print("\n")
    print("\n")
    print("Bibliography: ")
    print(bibliography)

user_input=input("Enter a topic, and a research article will be produced, with citations: ")
extract(user_input)
