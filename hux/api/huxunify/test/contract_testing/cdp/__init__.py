"""Set up for pact between HUX and CDP."""
from pact import Consumer, Provider
from pathlib import Path

import atexit

import huxunify.test.constants as t_c
from huxunify.test.contract_testing.utils import upload_pact_files_to_s3

# folder where generated pacts are stored
contracts_folder = Path(__file__).parent.parent.parent.parent.joinpath(
    t_c.CONTRACTS_FOLDER)

hux_cdp_pact = Consumer(t_c.HUX).has_pact_with(Provider(t_c.CDP),
                                               pact_dir=str(contracts_folder))
hux_cdp_pact.start_service()

atexit.register(upload_pact_files_to_s3, folder=contracts_folder)
atexit.register(hux_cdp_pact.stop_service)
