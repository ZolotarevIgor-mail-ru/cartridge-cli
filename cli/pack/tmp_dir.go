package pack

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/apex/log"

	"github.com/tarantool/cartridge-cli/cli/common"
	"github.com/tarantool/cartridge-cli/cli/project"
)

const (
	defaultHomeDir      = "/home"
	tmpPackDirNameFmt   = "pack-%s"
	defaultBuildDirName = "cartridge.tmp"
	packageFilesDirName = "package-files"
)

var (
	defaultCartridgeTmpDir string
)

func init() {
	homeDir, err := common.GetHomeDir()
	if err != nil {
		homeDir = defaultHomeDir
	}

	defaultCartridgeTmpDir = filepath.Join(homeDir, ".cartridge/tmp")
}

// tmp directory structure:
// ~/.cartridge/tmp/            <- projectCtx.CartridgeTmpDir (can be changed by CARTRIDGE_TEMPDIR)
//   pack-s18h29agl2/           <- projectCtx.TmpDir (projectCtx.PackID is used)
//     package-files/           <- PackageFilesDir
//       usr/share/tarantool
//       ...
//     tmp-build-file           <- additional files used for building the application

func detectTmpDir(projectCtx *project.ProjectCtx) error {
	var err error

	if projectCtx.CartridgeTmpDir == "" {
		// tmp dir wasn't specified
		projectCtx.CartridgeTmpDir = defaultCartridgeTmpDir
	} else {
		// tmp dir was specified
		projectCtx.CartridgeTmpDir, err = filepath.Abs(projectCtx.CartridgeTmpDir)
		if err != nil {
			return fmt.Errorf(
				"Failed to get absolute path for specified temporary dir %s: %s",
				projectCtx.CartridgeTmpDir,
				err,
			)
		}

		if fileInfo, err := os.Stat(projectCtx.CartridgeTmpDir); err == nil {
			// directory is already exists

			if !fileInfo.IsDir() {
				return fmt.Errorf(
					"Specified temporary directory is not a directory: %s",
					projectCtx.CartridgeTmpDir,
				)
			}

			// This little hack is used to prevent deletion of user files
			// from the specified tmp directory on cleanup.
			projectCtx.CartridgeTmpDir = filepath.Join(projectCtx.CartridgeTmpDir, defaultBuildDirName)

		} else if !os.IsNotExist(err) {
			return fmt.Errorf(
				"Unable to use specified temporary directory %s: %s",
				projectCtx.CartridgeTmpDir,
				err,
			)
		}
	}

	tmpDirName := fmt.Sprintf(tmpPackDirNameFmt, projectCtx.PackID)
	projectCtx.TmpDir = filepath.Join(projectCtx.CartridgeTmpDir, tmpDirName)

	return nil
}

func initTmpDir(projectCtx *project.ProjectCtx) error {
	if _, err := os.Stat(projectCtx.TmpDir); err == nil {
		log.Debugf("Tmp directory already exists. Cleaning it...")

		if err := common.ClearDir(projectCtx.TmpDir); err != nil {
			return fmt.Errorf("Failed to cleanup build dir: %s", err)
		}
	} else if !os.IsNotExist(err) {
		return fmt.Errorf("Unable to use temporary directory %s: %s", projectCtx.TmpDir, err)
	} else if err := os.MkdirAll(projectCtx.TmpDir, 0755); err != nil {
		return fmt.Errorf("Failed to create temporary directory %s: %s", projectCtx.TmpDir, err)
	}

	projectCtx.PackageFilesDir = filepath.Join(projectCtx.TmpDir, packageFilesDirName)

	if err := os.MkdirAll(projectCtx.PackageFilesDir, 0755); err != nil {
		return fmt.Errorf(
			"Failed to create package files directory %s: %s",
			projectCtx.PackageFilesDir,
			err,
		)
	}

	return nil
}