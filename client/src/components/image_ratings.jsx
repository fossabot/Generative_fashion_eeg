import React, { useState, useEffect } from 'react';
import DiscreteSlider from './discreteslider';
import { Button, IconButton, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import DeleteIcon from '@mui/icons-material/Delete';

export default function ImageRatingComponent() {

    // Anfängliche Beispielbilder (werden später durch generierte Bilder ersetzt)
    const defaultImages = [
        "images/original.png",
        "images/img_lila_6.5430.png",
        "images/img_white_6.3124.png",
        "images/img_blue_6.7962.png",
    ];

    const [currentIteration, setCurrentIteration] = useState(0);
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [newRating, setNewRating] = useState(0);
    const [count, setCount] = useState(0);
    const [hasRated, setHasRated] = useState(false);
    const [openAlert, setOpenAlert] = useState(false);
    const [alertMessage, setAlertMessage] = useState("");
    const [alertTitle, setAlertTitle] = useState("");
    const [currentImages, setCurrentImages] = useState(defaultImages);
    const [userId, setUserId] = useState(1);
    const [ratedImages, setRatedImages] = useState({});
    const [userDataInitialized, setUserDataInitialized] = useState(false);
    const [isResetting, setIsResetting] = useState(false);

    // Laden/Erstellen Benutzerdaten, immer aufgerufen, wenn komponente geladen oder sich in dem Abhängigkeiten der Arrays
    // am ende was ändert
    useEffect(() => {
        // Überprüfen, ob gerade zurückgesetzt wird - in diesem Fall nichts tun
        if (isResetting) {
            return;
        }
        // wiederholte inizialisierung verhindern
        if (!userDataInitialized) {
            // User-ID aus lokalen Speicher?
            const savedUserId = localStorage.getItem('currentUserId');
            // zuvorgespiecherte nutzer ID aus lokalem speicher
            if (savedUserId) {
                const parsedId = parseInt(savedUserId, 10);
                setUserId(parsedId);

                //  Bewertungen für nutzer vom Server laden
                loadUserData(parsedId);
                // Benutzer daten jetzt initialisiert
                setUserDataInitialized(true);
            } else {
                // keine ID? Dann neuen Nutzer erstellen
                createNewUserFile();
            }
        }
    }, [userDataInitialized, isResetting]);

    // rufe endpunkt auf, der die Bewertungsdaten für User X abruft
    const loadUserData = (id) => {
        fetch(`http://127.0.0.1:5000/ratings/${id}`)
            // HTTP Response -> Json & .then für asynchrone Antwortverarbeitung
            .then(response => response.json())
            .then(data => {
                // Konviertiertes Json als data object + Hauptlogik
                console.log(`Bewertungsdaten für Benutzer ${id} geladen:`, data);
                //  speichert später alle bewerteten Bilder, um schnell zu übersprüfen ob schon bewertet
                const ratedImagesMap = {};

                //  object durchgehen
                Object.keys(data).forEach(iterKey => {
                    // Iterationsschlüssel extrahieren (z.B. it0, it1, -> 0,1)
                    const iteration = iterKey.replace("it", "");
                    // Für jedes Bild entsprechenden Key setzen  der bestimmten It.
                    //Prüft, ob der Iterationsschlüssel im Datenobjekt existiert und ob er einen index - Array enthält
                    // verhindert Fehler, falls die Datenstruktur nicht der erwarteten Form entspricht

                    if (data[iterKey] && data[iterKey].index) {
                        // iteration über bild indizes die bereits bewertet wurden
                        data[iterKey].index.forEach((imageIndex, idx) => {
                            //schlüssel für beewertetes Bild
                            const key = `${iteration}_${imageIndex}`;
                            //makiert als bewertet
                            ratedImagesMap[key] = true;
                        });
                    }
                });

                //höchste It finden und setzen
                let highestIteration = 0;
                //höchste it finden
                Object.keys(data).forEach(iterKey => {
                    //wieder it nr in zahl umwandeln basis 10 für korrekte umwandlung
                    const iteration = parseInt(iterKey.replace("it", ""), 10);
                    //korret und aktuelle höher als biher höchste?
                    if (!isNaN(iteration) && iteration > highestIteration) {
                        // setze wert
                        highestIteration = iteration;
                    }
                });

                // Map aller Bilder in Rated Images
                setRatedImages(ratedImagesMap);
                //setzte it auf höchst gefundene 
                setCurrentIteration(highestIteration);

                // Schlüssel für die höchste It
                const currentIterKey = `it${highestIteration}`;

                // Wenn höchste It 0
                if (highestIteration === 0) {
                    // Dann nehme aktuell Die Standart Bilder aus dem public/images Ordner
                    setCurrentImages(defaultImages);
                }
                // Für höhere Iterationen also verwende generierte Bilder
                else if (data[currentIterKey] && data[currentIterKey].images) {
                    // Server-URL 
                    const serverImages = data[currentIterKey].images.map(
                        // URLS zeigen direkt auf Bildresourcen auf dem Server
                        img => `http://127.0.0.1:5000/images/${img}`
                    );
                    // Aktualisieren mit Server-Pfaden
                    setCurrentImages(serverImages);
                }
            })
            .catch(error => console.error(`Fehler beim Laden der Bewertungen für Benutzer ${id}:`, error));
    };

    // Lädt user daten automatisch neu wenn sich die Ähngen userId oder userDataInitialized ändern
    // Wichtig z.B. bei Reset, Aktuelle Daten neu gerendert werden oder New User angelegt wird
    useEffect(() => {
        if (userDataInitialized && userId) {
            loadUserData(userId);
        }
    }, [userId, userDataInitialized]);


  // Erstellung automatisch beim Laden oder manueller Nutzerklick
    const createUserCommon = (isManualCreation = false) => {
        // Wenn manuelle Erstellung, dann Reset-Prozess aktivieren
        if (isManualCreation) {
            //andere automatische Initialisierungen verhindern
            setIsResetting(true);
        }

        // Post-Anfrage -> Erstellen neuen Benutzers
        fetch("http://127.0.0.1:5000/create_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({})
        })
            .then(response => response.json())
            //json als data Objekt 
            .then(data => {
                console.log("Neuer Benutzer erstellt:", data);
                const newUserId = data.userId;

                // State-Updates
                localStorage.setItem('currentUserId', newUserId.toString());
                setUserId(newUserId);
                setRatedImages({});
                setUserDataInitialized(true);
                setCurrentIteration(0);
                setCount(0);
                setCurrentImageIndex(0);
                setHasRated(false);
                setNewRating(0);
                // Aktuell nut für default später nicht mehr
                setCurrentImages(defaultImages);

                // Zusätzliche Aktionen nur bei manueller Erstellung
                if (isManualCreation) {
                    setIsResetting(false);
                    setAlertTitle("New User Created");
                    setAlertMessage(`User ${newUserId} was successfully created. The iteration starts again at 0.`);
                    setOpenAlert(true);
                }
            })
            .catch(error => {
                if (isManualCreation) {
                    setAlertTitle("Error");
                    setAlertMessage("There was an error creating a new user. Please try again.");
                    setOpenAlert(true);
                    setIsResetting(false);
                }
            });
    };

    // Automatische Erstellung beim ersten Laden
    const createNewUserFile = () => {
        createUserCommon(false);
    };

    // Manuelle Erstellung durch Benutzerinteraktion
    const handleNewUser = () => {
        createUserCommon(true);
    };

    const handleAddRating = () => {
        // Bild bereits bewertet ? Erstelle Schlüssel für das aktuelle Bild,
        //  aus der Iteration und dem Bildindex
        const imageKey = `${currentIteration}_${currentImageIndex}`;

        //Aktuelles Bild gerated? Sende alterts -> keine Doppelbewertungen
        if (ratedImages[imageKey]) {
            setAlertTitle("Image has already been rated");
            setAlertMessage("This image has already been rated. Please go to the next picture.");
            setOpenAlert(true);
            return;
        }

        // Verhindern zusätzlicher Bewertungen nochmal markieren um sicher zu gehen
        setRatedImages(prev => ({ ...prev, [imageKey]: true }));

        fetch("http://127.0.0.1:5000/ratings", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                rating: newRating,
                imageIndex: currentImageIndex,
                iteration: currentIteration,
                userId: userId
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Bild als bewertet markieren
                setRatedImages(prev => ({ ...prev, [imageKey]: true }));
                setCount(count + 1);
                setHasRated(true);

                // Neue Bilder für die nächste Iteration setzen, wenn vorhanden
                if (data.newImagesAvailable && data.images) {
                    const serverImages = data.images.map(
                        img => `http://127.0.0.1:5000/images/${img}`
                    );

                
                }

                // Nach 4 Bewertungen zur nächsten Iteration
                if (count === 3) {
                    additeration();
                    setCount(0);

                    // Wenn wir eine neue Iteration beginnen, laden wir die neuen Bilder
                    if (data.newImagesAvailable && data.images) {
                        const serverImages = data.images.map(
                            img => `http://127.0.0.1:5000/images/${img}`
                        );
                        setCurrentImages(serverImages);
                        console.log("Neue Bilder:", serverImages);
                    }
                }
            })
            .catch(error => console.error("Error sending data:", error));
    };

    const handleNoOpinion = () => {
        // schlüssel für aktuelles Bild sowie in add rating
        const imageKey = `${currentIteration}_${currentImageIndex}`;
        if (ratedImages[imageKey]) {
            // wieder altert, wenn schon bewertet
            setAlertTitle("Image has already been rated");
            setAlertMessage("This picture has already been rated. Please go to the next picture.");
            setOpenAlert(true);
            return;
        }

        // Verhindern zusätzlicher Bewertungen
        setRatedImages(prev => ({ ...prev, [imageKey]: true }));

        fetch("http://127.0.0.1:5000/ratings", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                rating: "NaN",
                imageIndex: currentImageIndex,
                iteration: currentIteration,
                userId: userId
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Bild als bewertet markieren, sichterstellen das richtig im state 
                setRatedImages(prev => ({ ...prev, [imageKey]: true }));
                // Zähler des bewerteten Bildes um 1 erhöhen
                setCount(count + 1);
                // Benutzer hat Bild bewertet, state ist für navigation
                setHasRated(true);

                // Neue Bilder für die nächste Iteration setzen
                if (data.newImagesAvailable && data.images) {
                    const serverImages = data.images.map(
                        //Bildpfade mit Server URL ergänzen
                        img => `http://127.0.0.1:5000/images/${img}`
                    );
               
                }

                // Nach 4 Bewertungen zur nächsten Iteration 
                if (count === 3) { 
                    additeration();
                    // setzte count zurück
                    setCount(0);

                    //Neue It, lade neuen Bilder
                    if (data.newImagesAvailable && data.images) {
                        const serverImages = data.images.map(
                            img => `http://127.0.0.1:5000/images/${img}`
                        );
                        setCurrentImages(serverImages);
                    }
                }
            })
            .catch(error => console.error("Error sending data:", error));
    };

    // setzte ratings zurück
    const resetRating = () => {
        setNewRating(0);
        setHasRated(false);
    };

    const nextImage = () => {
        //Falls noch nicht bewertet
        if (!hasRated) {
            // für identifikation wieder
            const imageKey = `${currentIteration}_${currentImageIndex}`;
            if (ratedImages[imageKey]) {
                // Bild bereits bewertet -> zum nächsten Bild, % um in den Grenzen zu bleiben
                setCurrentImageIndex((prevIndex) => (prevIndex + 1) % currentImages.length);
                setNewRating(0);
                setHasRated(false);
            } else {
                // Zeige Warnung
                setAlertTitle("Please rate the picture first");
                setAlertMessage("You must first submit a rating or select \"No Opinion\" before you can switch to the next image.");
                setOpenAlert(true);
            }
            return;
        }
        
        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % currentImages.length);
        setNewRating(0);
        setHasRated(false);
    };

    const prevImage = () => {
        if (!hasRated) {
            // Prüfen, ob das aktuelle Bild bereits in einer früheren Sitzung bewertet wurde
            const imageKey = `${currentIteration}_${currentImageIndex}`;
            if (ratedImages[imageKey]) {
                // Bild wurde bereits bewertet, erlaube Navigation
                setCurrentImageIndex((prevIndex) =>
                    prevIndex === 0 ? currentImages.length - 1 : prevIndex - 1
                );
                setNewRating(0);
                setHasRated(false);
            } else {
                // Bild wurde noch nicht bewertet, zeige Warnung
                setAlertTitle("Please rate the picture first");
                setAlertMessage("You must first submit a rating or select \"No Opinion\" before you can switch to the previous image    .");
                setOpenAlert(true);
            }
            return;
        }

        setCurrentImageIndex((prevIndex) =>
            prevIndex === 0 ? currentImages.length - 1 : prevIndex - 1
        );
        setNewRating(0);
        setHasRated(false);
    };

    //Alert schließen
    const handleCloseAlert = () => {
        setOpenAlert(false);
    };

    // Iteration erhöhen
    const additeration = () => {
        setCurrentIteration(prevIteration => {
            const newIteration = prevIteration + 1;
            console.log(`Iteration wird erhöht von ${prevIteration} auf ${newIteration}`);
            return newIteration;
        });
    };

    const resetUserID = () => {
    
        setAlertTitle("Reset user IDs");
        setAlertMessage("All user data will be deleted! This action cannot be undone. Do you want to proceed?");

        // Dialog öffnen und auf Bestätigung warten
        const executeReset = () => {
            // Markiere Reset-Prozess aktiv 
            setIsResetting(true);

         
            setRatedImages({});
            setCurrentIteration(0);
            setCount(0);
            setCurrentImageIndex(0);
            setHasRated(false);
            setNewRating(0);

            // API-Aufruf zum Löschen von allen Dateien
            fetch("http://127.0.0.1:5000/delete_all_userIDs", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Alle Benutzerdaten gelöscht:", data);

                  
                    setAlertTitle("Confirmation");
                    setAlertMessage("All user data has been deleted. A first new user is created...");
                    setOpenAlert(true);

                    // Lokalen Speicher leeren, damit kein anderer Prozess zwischendurch einen Benutzer erstellt
                    localStorage.removeItem('currentUserId');

                    // Sicherstellen -> keine race condition 
                    setTimeout(() => {
                        // Direk neuen Benutzer zu erstellen
                        fetch("http://127.0.0.1:5000/create_user", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({})
                        })
                            .then(response => response.json())
                            .then(userData => {
                               

                                handleCloseAlert();
                                setAlertTitle("Confirmation");
                                setAlertMessage(`New user with ID ${userData.userId} has been created.`);
                                setOpenAlert(true);

                                // User-ID setzen
                                const newId = userData.userId;
                                localStorage.setItem('currentUserId', newId.toString());
                                setUserId(newId);

                                // Reset-Prozess ist deaktiviert
                                setIsResetting(false);
                                setUserDataInitialized(true);
                            })
                            .catch(err => {
                                setAlertTitle("Error");
                                setAlertMessage(`Error when creating a new user: ${err.message}`);
                                setOpenAlert(true);

                                // Auch bei Fehler Reset-Prozess beenden
                                setIsResetting(false);
                            });
                    }, 1000);
                })
                .catch(error => {
                    console.error("Error when deleting user data :", error);
                    setAlertTitle("Error");
                    setAlertMessage(`Error when deleting user data: ${error.message}. Please try again.`);
                    setOpenAlert(true);
                });
        };

        // Benutzer nach Bestätigung fragen
        if (window.confirm("Do you really want to delete all user data? This process cannot be undone.")) {
            // Sicherstellen, dass keine anderen Anfragen laufen
            executeReset();
        }
    };

    // ########## UI ####################
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            // height: '100vh',
            width: '100%',
        }}>

            <div style={{ display: 'flex', position: 'absolute', top: '10px', left: '10px' }}>
                <Button
                    onClick={handleNewUser}
                    variant="contained"
                    color="primary"
                    startIcon={<PersonAddIcon />}
                    size="small"
                >
                    New User (ID: {userId})
                </Button>
                <Button
                    onClick={resetUserID}
                    variant="contained"
                    color="error"
                    startIcon={<DeleteIcon />}
                    size="small"
                    style={{ marginLeft: '10px' }}
                >
                    Delete all Users
                </Button>
            </div>

            <div style={{
                position: 'relative',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%',
                maxWidth: '600px'
            }}>

                <IconButton
                    onClick={prevImage}
                    style={{
                        position: 'absolute',
                        left: '-15px',
                        backgroundColor: 'rgba(0,0,0,0.2)',
                        padding: '5px',
                        zIndex: 1
                    }}
                >
                    <ChevronLeftIcon style={{ color: 'white' }} />
                </IconButton>


                <div style={{ width: '100%', textAlign: 'center' }}>
                    <img
                        src={currentImages[currentImageIndex]}
                        alt={`Bild ${currentImageIndex + 1}`}
                        style={{ maxWidth: '100%', maxHeight: '50vh', padding: '5px' }}
                    />
                </div>


                <IconButton
                    onClick={nextImage}
                    style={{
                        position: 'absolute',
                        right: '-15px',
                        backgroundColor: 'rgba(0,0,0,0.2)',
                        padding: '5px',
                        zIndex: 1
                    }}
                >
                    <ChevronRightIcon style={{ color: 'white' }} />
                </IconButton>
            </div>


            <div style={{ width: '100%', maxWidth: '400px', margin: '20px 0' }}>
                <DiscreteSlider onChange={(value) => setNewRating(value)} value={newRating} />
            </div>


            <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
                <Button
                    onClick={handleAddRating}
                    variant="contained"
                    color="primary"
                >
                    Confirm Rating
                </Button>

                <Button
                    onClick={handleNoOpinion}
                    variant="outlined"
                    color="primary"
                >
                    No Opinion
                </Button>

                <IconButton
                    onClick={resetRating}
                    color="default"
                    title="Bewertung zurücksetzen"
                >
                    <RestartAltIcon />
                </IconButton>
            </div>

            <Dialog
                open={openAlert}
                onClose={handleCloseAlert}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">
                    {alertTitle || "Hinweis"}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText id="alert-dialog-description">
                        {alertMessage || "Es ist ein Fehler aufgetreten."}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseAlert} color="primary" autoFocus>
                        OK
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}