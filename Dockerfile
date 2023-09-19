FROM toolbelt/dig 

ENTRYPOINT dig +short txt ch whoami.cloudflare @1.0.0.1

