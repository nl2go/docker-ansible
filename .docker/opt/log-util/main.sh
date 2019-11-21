#!/bin/bash

locationDir='<%= @location_dir %>'

error='ERROR'
warn='WARN '
info='INFO '
debug='DEBUG'
logLocation='/dev/null'

function info()
{
    log "$1" "$info" "$logLocation" "$2"
}

function debug()
{
    log "$1" "$debug" "$logLocation" "$2"
}

function error()
{
    log "$1" "$error" "$logLocation" "$2"
}

function warn()
{
    log "$1" "$warn" "$logLocation" "$2"
}

function log()
{
	local logMsg="$1"
	local level="$2"
	local location="$3"

	local source="$4"
	if [ -z "$source" ]; then
		source=$(basename "$0")
	fi

	local outMsg="$logMsg"
	local dateTime=$(date "+%Y-%m-%d %H:%M:%S")

	local green='\e[92m'
	local red='\e[31m'
	local white='\e[0m'
	local yellow='\e[33m'

	case "$level" in
	"$info")
	    outMsg="$green$outMsg$white"
	    ;;
	"$warn")
	    outMsg="$yellow$outMsg$white"
	    ;;
	"$error")
	    outMsg="$red$outMsg$white"
	    ;;
	*)
	    ;;
	esac

	echo -e "$outMsg"

	if [ -n "$location" ]; then
		echo -e "$dateTime $level [$source]:\t$logMsg" >> $location
	fi
}
