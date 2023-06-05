import logging
from pathlib import Path


# Flexible event logging system

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Logging setting and creation of log file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=BASE_DIR / 'backend.log',
                    )

# logging.debug("La fonction a bien été exécutée")
# logging.info("Message d'information général")
# logging.warning("Attention !")
# logging.error("Une erreur est arrivée")
# logging.critical("Erreur critique")
