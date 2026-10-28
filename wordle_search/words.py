"""The word list (common five-letter English words). Anything that isn't exactly five letters is dropped."""
RAW = """
about above actor adult after again agree ahead alarm alert alive allow alone angel anger angry apple
arena argue arise armor aside avoid awake aware baker basic beach begin below bench birth black blame
blank blast blind block blood board brain brand brave bread break brick bride brief bring broad brown
brush build bunch cabin candy carry catch cause chain chair chalk charm chart chase cheap check chest
chief child chill civil claim class clean clear clerk click cliff climb clock close cloth cloud coach
coast color could count court cover crack craft crane crash crazy cream crime cross crowd crown curve
cycle daily dance death delay depth dirty doubt dozen draft drama dream dress drift drink drive eager
early earth eight elite empty enemy enjoy enter equal error event every exact extra faith false fancy
fault feast fence fever field fifth fight final first flame flash fleet float flood floor flour focus
force forth found frame fresh front frost fruit giant given glass globe glory grace grade grain grand
grape grass great green greet group guard guess guest guide habit happy harsh heart heavy honey honor
horse hotel house human humor ideal image index inner issue ivory jelly joint judge juice knife label
large laser later laugh layer learn least leave legal lemon level light limit local logic loose lower
lucky lunch magic major march match maybe media mercy metal might minor model money month moral motor
mount mouse mouth movie music nerve never night noble noise north novel nurse ocean offer often olive
onion opera orbit order other outer owner paint panel paper party pasta patch pause peace pearl phase
phone photo piano piece pilot pitch pizza place plain plane plant plate point pound power press price
pride prime print prize proof proud pulse quick quiet radio raise range rapid ratio reach ready realm
relax reply ridge right rival river robot rough round route royal salad sauce scale scene score sense
serve seven shade shake shape share sharp sheep sheet shelf shell shift shine shirt shock shoot shore
short sight since skill sleep slice slide small smart smile smoke snake solar solid solve sound south
space spare speak speed spell spend spice split sport staff stage stair stand start state steak steel
stick still stock stone store storm story study stuff style sugar sunny sweet swift swing table taste
teach thank theme thick thing think three throw thumb tiger tight title toast today tooth topic total
touch tough tower trace track trade trail train treat trend trial trick truck trust truth twice uncle
under union upper urban usual valid value video visit vital voice waste watch water weary weigh whale
wheat wheel where which while white whole woman world worry worth would write wrong yield young youth
zebra
"""
WORDS = sorted({w for w in RAW.split() if len(w) == 5 and w.isalpha()})
