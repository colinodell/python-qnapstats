## [0.6.2](https://github.com/colinodell/python-qnapstats/compare/0.6.1...0.6.2) (2026-10-17)


### Bug Fixes

* return the retried response when a GET request is retried ([7eec477](https://github.com/colinodell/python-qnapstats/commit/7eec477aa97e9dd178095ec79f246f1a965e60b9))

## [0.6.1](https://github.com/colinodell/python-qnapstats/compare/0.6.0...0.6.1) (2026-10-17)

### Bug Fixes

* skip incomplete NIC entries in system stats ([#110](https://github.com/colinodell/python-qnapstats/issues/110)) ([52de985](https://github.com/colinodell/python-qnapstats/commit/52de985958827fa3eb366674c73fe926f5efb325))
* fix KeyError when sys_tempc/sys_tempf are missing from system stats ([#109](https://github.com/colinodell/python-qnapstats/issues/109))
* fall back to the legacy bandwidth API when QSM40bandwidth returns no data ([#112](https://github.com/colinodell/python-qnapstats/issues/112))

### Python Support

* drop Python 3.5 and 3.6; `python_requires` is now `>=3.7` ([#113](https://github.com/colinodell/python-qnapstats/issues/113))
* test against Python 3.10 through 3.15 ([#113](https://github.com/colinodell/python-qnapstats/issues/113))

### Documentation

* add TS-464 and TS-439 Pro II+ to supported models ([#102](https://github.com/colinodell/python-qnapstats/issues/102), [#105](https://github.com/colinodell/python-qnapstats/issues/105))

# [0.6.0](https://github.com/colinodell/python-qnapstats/compare/0.5.0...0.6.0) (2025-06-25)


### Features

* adding system fan monitoring ([#98](https://github.com/colinodell/python-qnapstats/issues/98)) ([e9254ee](https://github.com/colinodell/python-qnapstats/commit/e9254eec25f72802d17a34f09a47c1f80039f8fd))

# [0.5.0](https://github.com/colinodell/python-qnapstats/compare/0.4.0...0.5.0) (2022-06-07)


### Bug Fixes

* add missing token ([2b9eefa](https://github.com/colinodell/python-qnapstats/commit/2b9eefa1f901e96f02ed56b54239bdab4fd88d7c))
* change main branch in releaserc.json ([c976249](https://github.com/colinodell/python-qnapstats/commit/c9762495395ff8586fac643e0ecc5f8405dad30d))


### Features

* add external devices informations ([508f385](https://github.com/colinodell/python-qnapstats/commit/508f3850d9ced07d4a9a33829c2b7f5264929c64))
* add external devices informations ([1b73056](https://github.com/colinodell/python-qnapstats/commit/1b73056035480f9d26755f6a3a7c0ab551cdbf0d))
