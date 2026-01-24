import argparse
import sys
import time
import logging
from core.engine import ScanningEngine

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("aegisscan.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

from core.config import Config
from core.mission import MissionTypes

def main():
    parser = argparse.ArgumentParser(description="AegisScan Strategic: Adversarial Simulation Platform")
    parser.add_argument("target", help="Target host")
    parser.add_argument("-m", "--mode", default=Config.MODE_AUDIT, choices=[Config.MODE_AUDIT, Config.MODE_STEALTH, Config.MODE_OBSERVATION], help="Operational Mode")
    parser.add_argument("--mission", default=MissionTypes.RECON, choices=[MissionTypes.RECON, MissionTypes.VALIDATION, MissionTypes.EMULATION], help="Strategic Mission Objective")
    parser.add_argument("-d", "--depth", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument("-i", "--interval", type=int, default=0, help="Scan interval in minutes")
    parser.add_argument("-o", "--output", default="text", choices=["text", "json", "both"])
    parser.add_argument("--stealth", action="store_true", help="Legacy stealth flag (overrides mode if set)")
    
    args = parser.parse_args()
    setup_logging()
    logger = logging.getLogger("AegisScan")

    # Validate Mode (v3.0 Hardening)
    Config.validate_mode(args.mode)
    
    print("------------------------------------------------------------")
    print(f"AEGISSCAN STRATEGIC v4.0 - MODE: {args.mode.upper()} | MISSION: {args.mission}")
    print("------------------------------------------------------------")
    
    engine = ScanningEngine(
        args.target, 
        args.depth, 
        args.output, 
        mode=args.mode, 
        mission_type=args.mission, 
        stealth=args.stealth
    )
    
    try:
        if args.interval > 0:
            logger.info(f"Continuous mode enabled. Interval: {args.interval} minutes.")
            while True:
                engine.run()
                logger.info(f"Scan completed. Waiting {args.interval} minutes for next cycle...")
                time.sleep(args.interval * 60)
        else:
            engine.run()
            logger.info("Scan completed successfully.")
            
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Critical error during scan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
