# Cloud setup guide
Dette er en guide som beskriver hvordan man kan sette opp en conteiner i azure med az client. Man kan også gjøre mye av dette gjennom det grafiske grensesnittet i azure portal, men det er veldig tregt.

NB: denne guiden viser ikke "best practice", men er en enkel måte å sette opp en konteiner kjapt i skyen.

## Du trenger
* en konto i azure. 
* en konto i dockerhub. https://hub.docker.com/

## Fremgangsmåte
### Dockerhub
logginn i dockerhub og lag et nytt repository. Set dette til public. Da slipper vi å styre med autentisering.

Kall dette repositoriet det du vil. I denne guiden heter det `johan`.


Vi ønsker å legge ut en dockerimage i vårt nylagde repo. Derfor må vi bygge det lokalt og derretter publisere det.



hvordan docker build fungerer
```sh

docker build -t <brukernavn>/<reponame>:<tag> .
```
Eksempel:

```sh

docker build -t martinstudent2/johan:latest .
```

logg inn i dockerhub.
```sh

docker login
```

Publiser bildet
```sh

docker push martinstudent2/johan:latest
```

Perfekt! Nå er bildet tilgjenglig for alle i verden, og nå skal vi bruke det i azure.

## Azure
Logg in i azure med az client
```sh
az login
```

name: navnet på ressursgruppen
location: hvor i verden skal ressursene i denne gruppen kjøre
Lag en ressurs gruppe som conteineren skal kjøre i
```sh
az group create --name johan --location northeurope

```

Lag en conteiner i azure. 
* resource-group: navnet på ressursgruppen
* name: navnet på konteineren
* image: navnet på docker bilde som ligger i dockerhub
* dns-name-lable: navnet på tjenesten - "navn".northeurope.azurecontainer.io (dette MÅ være unikt, så "johaneersus" er opptatt ;))
* ports: hvilke porter som eksponeres i kontaineren
```sh
az container create --resource-group johan --name johandemo --image martinstudent2/johan --dns-name-label johaneersus --ports 8000

```

se statusen på konteineren

```sh
az container show --resource-group johan --name johandemo --query "{FQDN:ipAddress.fqdn ProvisioningState:provisioningState}" --out table

```


Hvis statusen er OK, så bør alt være greit. Gå inn på nettsiden deres:

http://johaneersus.northeurope.azurecontainer.io:8000/

http://"dns-name-lable".northeurope.azurecontainer.io:8000/


## SHIT wi gjorde noe feil i azure!
Ikke noe problem. da kan man slette ressursgruppen sin og starte på nytt.
```

az group delete --name johan
```

## Videre arbeid:
1. Hvordan skal man oppdatere denne konteineren i skyen når konden endrer seg? (Tips. CICD eller webhooks i azure)

