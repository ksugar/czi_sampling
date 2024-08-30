# CZI sampling for the evaluation of the optimal imaging conditions for the tracking analysis using ELEPHANT

## Install

### pip

The following command will install the module from the main branch on the GitHub repository.

```bash
python -m pip install git+https://github.com/ksugar/czi_sampling
```

## Usage

### Example dataset

```txt
$ tree movie1-16.czi
movie1-16.czi/
 ├── movie1-16_AcquisitionBlock1.czi
 │   ├── movie1-16_AcquisitionBlock1_pt1.czi
 │   ├── movie1-16_AcquisitionBlock1_pt2.czi
 │   ├── movie1-16_AcquisitionBlock1_pt3.czi
 │   ├── movie1-16_AcquisitionBlock1_pt4.czi
 │   ├── movie1-16_AcquisitionBlock1_pt5.czi
 │   ├── movie1-16_AcquisitionBlock1_pt6.czi
 │   ├── movie1-16_AcquisitionBlock1_pt7.czi
 │   ├── movie1-16_AcquisitionBlock1_pt8.czi
 │   ├── movie1-16_AcquisitionBlock1_pt9.czi
 │   └── movie1-16_AcquisitionBlock1_pt10.czi
 └── movie1-16.czmbi
```

### Run the script

```bash
run_sampling ./movie1-16.czi/movie1-16_AcquisitionBlock1.czi/ ../sampling_result/
```

### Output

```txt
sampling_result
├── 4E.tif
├── improved_t.tif
├── improved_z.tif
├── improved_zt1.tif
├── improved_zt2.tif
├── original.tif
└── standard.tif
```