# Cloud setup guide
Dette er en guide som beskriver hvordan man kan sette opp en conteiner i Azure med `docker` og `az client`. Man kan oppnå akkuratt det sammen gjennom det grafiske grensenittet i portal.azure.com, men det er mye kjappere å gjøre det gjennom terminalen. 

**NB: Denne guiden viser ikke "best practice", men viser en enkel måte å sette en konteiner kjapt opp i skyen.**

## Du trenger
* docker desktop
* az client (det finnes en annet klient spesifik for Powershell, men az client funker fint)
* en konto i Azure. 
* en konto i dockerhub. https://hub.docker.com/
* git skills 😎

## Fremgangsmåte for å sette opp
### Dockerhub
logg inn i dockerhub og lag et nytt public repository. Gi repoet et navn. I denne guiden heter den `johan`


> **Docker og dockerhub vedlig kort forklart**:
>
> Docker og dockerhub vedlig kort forklart: Docker er måte å lage/kjøre programmer i et isolert miljø. I dette prosjektet ønsker vi å lage en webserver som oppfører seg likt på vår engen datamaskin og i skyen. Docker er perfekt for det, og lar oss definere hvordan koden vår skal kjøre. ref: `Dockerfile`. Docker ser på Dockerfile filen og bygger det imaget vårt ut ifra hva vi har sagt. Når vi har bygget et docker image har vi det bare lokalt på vår egen pc, men siden vi ønsker å kjøre serveren i skyen må vi publisere imaget vårt i et container-registry. Nå bruker vi DockerHub siden det er lett å gjøre images offentlig tilgjengelig (slik at vi slipper å autentisere senere, når vi skal laste det ned igjen). 


Første steg når koden er klar og man ønsker å kjøre den i skyen er å bygge et docker-image. Da bruker man docker kommandoen `docker build`. For å forenkle prossessen senere kan vi bruke vår eget docker hub brukernavn og repo navn. I tillegg må man ha en tag, bruk "latest". Ikke glem punktum på slutten. Punktumet beskriver hvor docker skal bygge et image fra (jeg antar at dere er i prosjektet sit directory).

Ekstra 1: Klon ned repoet og bytt til denne branchen.

Ekstra 2: for å kjøre docker build (på denne måten), må man bruke terminalen til å kjøre kommandoer. Bruk terminalen til å navigere deg til github repoet.
`cd path/til/prosjekt`. Bruk kommandoen `pwd` for å sikre deg at du er på riktig sted. Du vil få noe sånt ut `path/til/prosjekt/Webserver`. Et annet alternativ når man bruker VSCode er å trykke på "terminal" -> "new terminal" i øverste menyen. Da kommer du i riktig kontekst og kan kjøre docker build som vist under.

```sh
docker build -t <brukernavn>/<reponame>:<tag> .
```

Eksempel: Min brukerkonto heter martinstudent2 og repoet mitt heter johan. Da vil det set sånn ut.
```sh
docker build -t martinstudent2/johan:latest .
```

Nå har du bygget bildet lokalt og kan testkjøre det før vi dytter det til dockerhub. Du kan spinne opp en conteiner av imaget sånn her.
Når det kjører gå til http://localhost:8000/ og sjekk om alt er ok.
```sh
docker run -p 8000:8000 martinstudent2/johan:latest
```

Hvis alt er ok og konteineren kjører som forventet kan vi publisere imaget. Logg inn i dockerhub i commandolinja.
```sh
docker login
```

Publiser bildet
```sh
docker push martinstudent2/johan:latest
```

Nå er bildet tilgjenglig for alle i verden! 🌎

## Azure
Vi har testet konteineren lokalt, men nå skal i kjøre den i skyen.

Logg in i azure med az client
```sh
az login
```

Lag en resource-group som conteineren skal kjøre i. En resource-group er måten vi samler infrastruktur i azure. Gruppen bestemmer hvor i hverden infrastrukturen skal kjøre. Vi velger å plasere infrastrukturen i nordeuropa. 
* name: navnet på ressursgruppen
* location: hvor i verden skal ressursene i denne gruppen kjøre
```sh
az group create --name johan --location northeurope
```

Nå skal vi lage en container i Azure. Dette kan sammenlignes med steget vi kjørte `docker run ...` commandoen, der vi brukte et image til å spinne opp en container.
* resource-group: navnet på ressursgruppen
* name: navnet på konteineren
* image: navnet på docker bilde som ligger i dockerhub
* dns-name-lable: navnet på tjenesten - "navn".northeurope.azurecontainer.io (dette MÅ være unikt, så "johaneersus" er opptatt ;))
* ports: hvilke porter som eksponeres i kontaineren
```sh
az container create --resource-group johan --name johandemo --image martinstudent2/johan --dns-name-label johaneersus --ports 8000
```

For å se statusen på containeren kan man kjøre denne kommandoen.
```sh
az container show --resource-group johan --name johandemo --query "{FQDN:ipAddress.fqdn ProvisioningState:provisioningState}" --out table
```

Hvis statusen er OK, så bør alt være greit. Gå inn på nettsiden deres:

http://johaneersus.northeurope.azurecontainer.io:8000/

http://"dns-name-lable".northeurope.azurecontainer.io:8000/

<br></br>
🌟 Bra jobba! Nå kan du skrive "Experience with building and deploying docker container with Azure Clound infrastrcuture and Docker Hub" på CV-en.
<br></br>

## SHIT vi gjorde noe feil i Azure!
Ikke noe problem. da kan man slette ressursgruppen sin og starte på nytt.
```
az group delete --name johan
```



## Endret koden?
Endret koden? Har du testet den lokalt og ønkser å kjøre den oppdaterte koden i skyen. Her et et forslag.

1. Bygg docker image på nytt.
2. Test at den fungerer lokalt.
3. Push image til Docker Hub
4. Oppdater conteineren i Azure med å kjøre samme create commando som dere deploya den med.


## Ekstra CV materiale
1. Sett opp automatisk bygging av bildet med Github CI/CD. Automatisk publiser et nytt docker image til dockerhub når noen publiserer kode i "main" branchen. Azure skal bruke en webhook for å redeploye konteineren når et nytt bilde blir publisert i Docker Hub. Hvis dere klarer dette kan dere skrive følgende på CV-en. "Experience with automatic deplyoment using CI/CD"

2. Ikke bruke docker hub registry, heller opprette en egen container registry i Azure.
