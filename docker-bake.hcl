group "default" {
  targets = ["trixie"]
}

target "base" {
  context = "."
  platforms = ["linux/amd64"]
}

target "trixie" {
  inherits = ["base"]
  dockerfile = "Dockerfile.trixie"
  tags = ["gebrauchtwagen:trixie"]
}

target "alpine" {
  inherits = ["base"]
  dockerfile = "Dockerfile.alpine"
  tags = ["gebrauchtwagen:alpine"]
}
