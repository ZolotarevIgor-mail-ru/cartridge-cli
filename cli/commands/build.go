package commands

import (
	"github.com/apex/log"
	"github.com/spf13/cobra"

	"github.com/tarantool/cartridge-cli/cli/build"
)

func init() {
	rootCmd.AddCommand(buildCmd)
}

var buildCmd = &cobra.Command{
	Use:   "build [PATH]",
	Short: "Build application for local development",
	Long:  "Build application in specified PATH (default \".\")",
	Args:  cobra.MaximumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		err := runBuildCommand(cmd, args)
		if err != nil {
			log.Fatalf(err.Error())
		}
	},
}

func runBuildCommand(cmd *cobra.Command, args []string) error {
	var err error

	projectCtx.Path = cmd.Flags().Arg(0)

	err = build.FillCtx(&projectCtx)
	if err != nil {
		return err
	}

	// build project
	err = build.Run(&projectCtx)
	if err != nil {
		return err
	}

	return nil
}