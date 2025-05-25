import React, { useState, useEffect } from 'react';
import DiscreteSlider from './discreteslider';
import { Button, IconButton, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import PersonAddIcon from '@mui/icons-material/PersonAdd';

export default function ImageRatingComponent() {

    const images = [
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
    const [userId, setUserId] = useState(1);
    const [ratedImages, setRatedImages] = useState({});
    const [userDataInitialized, setUserDataInitialized] = useState(false);

    // Beim ersten Laden User-ID oder neues File
    useEffect(() => {
        if (!userDataInitialized) {
            // User-ID aus dem lokalen Speicher?
            const savedUserId = localStorage.getItem('currentUserId');
            if (savedUserId) {
                const parsedId = parseInt(savedUserId, 10);
                console.log("Gespeicherte User-ID geladen:", parsedId);
                setUserId(parsedId);

                // bestehende Bewertungen für nutzer laden
                loadUserData(parsedId);
                setUserDataInitialized(true);
            } else {
                // neuen Nutzer erstellen
                console.log("Kein gespeicherter Benutzer gefunden, erstelle neuen Benutzer");
                createNewUserFile();
            }
        }
    }, [userDataInitialized]);

    //  Lade Benutzerdaten
    const loadUserData = (id) => {
        fetch(`http://127.0.0.1:5000/ratings/${id}`)
            .then(response => response.json())
            .then(data => {
                console.log(`Bewertungsdaten für Benutzer ${id} geladen:`, data);

                //  bereits bewertete Bilder makrieren
                const ratedImagesMap = {};

                //  Iterationen durchgehen
                Object.keys(data).forEach(iterKey => {
                    const iteration = iterKey.replace("it", "");
                    // Für jedes Bild den entsprechenden Key setzen in bestimmter It.
                    if (data[iterKey] && data[iterKey].index) {
                        data[iterKey].index.forEach((imageIndex, idx) => {
                            const key = `${iteration}_${imageIndex}`;
                            ratedImagesMap[key] = true;
                        });
                    }
                });

                //höchste  Iteration finden und setzen
                let highestIteration = 0;
                Object.keys(data).forEach(iterKey => {
                    const iteration = parseInt(iterKey.replace("it", ""), 10);
                    if (!isNaN(iteration) && iteration > highestIteration) {
                        highestIteration = iteration;
                    }
                });

                // Status aktualisieren
                setRatedImages(ratedImagesMap);
                setCurrentIteration(highestIteration);

                console.log(`Höchste Iteration für Benutzer ${id}: ${highestIteration}`);
                console.log("Bewertete Bilder geladen:", ratedImagesMap);
            })
            .catch(error => console.error(`Fehler beim Laden der Bewertungen für Benutzer ${id}:`, error));
    };

    // Laden bereits bewerteten Bilder bei Änderung der User-ID
    useEffect(() => {
        if (userDataInitialized && userId) {
            loadUserData(userId);
        }
    }, [userId, userDataInitialized]);

    // neues User-File
    const createNewUserFile = () => {
        fetch("http://127.0.0.1:5000/create_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({})
        })
            .then(response => response.json())
            .then(data => {
                console.log("Neuer Benutzer erstellt:", data);
                // User-ID in lokalen Speicher für später
                localStorage.setItem('currentUserId', data.userId.toString());
                setUserId(data.userId);
                setRatedImages({});
                setUserDataInitialized(true);
                setCurrentIteration(0);
                setCount(0);
                setCurrentImageIndex(0);
                setHasRated(false);
                setNewRating(0);
            })
            .catch(error => console.error("Fehler beim Erstellen eines neuen Benutzers:", error));
    };

    //  neuen User-Files mit der nächsten verfügbaren ID
    const handleNewUser = () => {
        // Erstellen einer neuen User-Datei ohne spezifische ID (Server wählt nächste freie ID)
        fetch("http://127.0.0.1:5000/create_user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({})
        })
            .then(response => response.json())
            .then(data => {
                console.log("Neuer Benutzer erstellt:", data);

                //User-ID aus der Antwort verwenden
                const newUserId = data.userId;

                // Löschen vorheriger Bewertungen 
                setRatedImages({});

                // Zurücksetzen der Iteration und des Zählers
                setCurrentIteration(0);
                setCount(0);

                // Zurücksetzen des aktuellen Bildes
                setCurrentImageIndex(0);

                // Zurücksetzen der Bewertung
                setNewRating(0);
                setHasRated(false);

                // User-ID im lokalen Speicher speichern
                localStorage.setItem('currentUserId', newUserId.toString());

                // User-ID im State setzen
                setUserId(newUserId);

                // Zeige eine Erfolgsmeldung
                setAlertTitle("Neuer Benutzer erstellt");
                setAlertMessage(`Benutzer ${newUserId} wurde erfolgreich erstellt. Die Iteration beginnt wieder bei 0.`);
                setOpenAlert(true);
            })
            .catch(error => {
                console.error("Fehler beim Erstellen eines neuen Benutzers:", error);
                setAlertTitle("Fehler");
                setAlertMessage("Es gab einen Fehler beim Erstellen eines neuen Benutzers. Bitte versuchen Sie es erneut.");
                setOpenAlert(true);
            });
    };

    const handleAddRating = () => {
        // Bild bereits bewertet ?
        const imageKey = `${currentIteration}_${currentImageIndex}`;
        if (ratedImages[imageKey]) {
            setAlertTitle("Bild wurde bereits bewertet");
            setAlertMessage("Dieses Bild wurde bereits bewertet. Bitte gehen Sie zum nächsten Bild.");
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
                rating: newRating,
                imageIndex: currentImageIndex,
                iteration: currentIteration,
                userId: userId
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log("Response from backend:", data);
                // Bild als bewertet markieren
                setRatedImages(prev => ({ ...prev, [imageKey]: true }));
                setCount(count + 1);
                setHasRated(true);

                // Nach 4 Bewertungen zur nächsten Iteration
                if (count === 3) { 
                    additeration();
                    console.log("Iteration erhöht auf:", currentIteration + 1);
                    setCount(0);
                }
            })
            .catch(error => console.error("Error sending data:", error));
    };

    const handleNoOpinion = () => {
        // Bild bereits bewertet ?
        const imageKey = `${currentIteration}_${currentImageIndex}`;
        if (ratedImages[imageKey]) {
            setAlertTitle("Bild wurde bereits bewertet");
            setAlertMessage("Dieses Bild wurde bereits von Ihnen bewertet. Bitte gehen Sie zum nächsten Bild.");
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
                console.log("Response from backend:", data);
                // Bild als bewertet markieren
                setRatedImages(prev => ({ ...prev, [imageKey]: true }));
                setCount(count + 1);
                setHasRated(true);

                // Nach 4 Bewertungen zur nächsten Iteration wechseln
                if (count === 3) { // Wenn dies die vierte Bewertung ist (count ist 0-basiert)
                    additeration();
                    console.log("Iteration erhöht auf:", currentIteration + 1);
                    setCount(0);
                }
            })
            .catch(error => console.error("Error sending data:", error));
    };

    const resetRating = () => {
        setNewRating(0);
        setHasRated(false);
    };

    const nextImage = () => {
        if (!hasRated) {
            // Prüfen, ob das aktuelle Bild bereits in einer früheren Sitzung bewertet wurde
            const imageKey = `${currentIteration}_${currentImageIndex}`;
            if (ratedImages[imageKey]) {
                // Bild wurde bereits bewertet, erlaube Navigation
                setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
                setNewRating(0);
                setHasRated(false);
            } else {
                // Bild wurde noch nicht bewertet, zeige Warnung
                setAlertTitle("Bitte bewerte zuerst das Bild");
                setAlertMessage("Du musst erst eine Bewertung abgeben oder \"Keine Meinung\" auswählen, bevor du zum nächsten Bild wechseln kannst.");
                setOpenAlert(true);
            }
            return;
        }

        setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
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
                    prevIndex === 0 ? images.length - 1 : prevIndex - 1
                );
                setNewRating(0);
                setHasRated(false);
            } else {
                // Bild wurde noch nicht bewertet, zeige Warnung
                setAlertTitle("Bitte bewerte zuerst das Bild");
                setAlertMessage("Du musst erst eine Bewertung abgeben oder \"Keine Meinung\" auswählen, bevor du zum vorherigen Bild wechseln kannst.");
                setOpenAlert(true);
            }
            return;
        }

        setCurrentImageIndex((prevIndex) =>
            prevIndex === 0 ? images.length - 1 : prevIndex - 1
        );
        setNewRating(0);
        setHasRated(false);
    };

    const handleCloseAlert = () => {
        setOpenAlert(false);
    };

    const additeration = () => {
        setCurrentIteration(prevIteration => {
            const newIteration = prevIteration + 1;
            console.log(`Iteration wird erhöht von ${prevIteration} auf ${newIteration}`);
            return newIteration;
        });
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            // height: '100vh',
            width: '100%',
        }}>
          
            <div style={{ position: 'absolute', top: '10px', left: '10px' }}>
                <Button
                    onClick={handleNewUser}
                    variant="contained"
                    color="secondary"
                    startIcon={<PersonAddIcon />}
                    size="small"
                >
                    Neuer Benutzer (ID: {userId})
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
                        src={images[currentImageIndex]}
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
                    Bewertung bestätigen
                </Button>

                <Button
                    onClick={handleNoOpinion}
                    variant="outlined"
                    color="primary"
                >
                    Keine Meinung
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