#!/usr/bin/env python3

import argparse
from hailo_platform import HEF


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect HEF input vstreams for all or specific networks."
    )

    parser.add_argument(
        "hef",
        type=str,
        help="Path to HEF file (mandatory)"
    )

    parser.add_argument(
        "--net",
        type=str,
        default=None,
        help="Optional: Inspect only a specific network name"
    )

    return parser.parse_args()


def inspect_hef(hef_path, net_filter=None):
    print(f"📦 Loading HEF: {hef_path}")
    hef = HEF(hef_path)

    networks = hef.get_networks_names()

    if net_filter and net_filter not in networks:
        print(f"❌ Network '{net_filter}' not found in HEF!")
        print("Available networks:")
        for n in networks:
            print("  •", n)
        return

    for net in networks:
        if net_filter and net != net_filter:
            continue

        print(f"\n=== 🧠 Network: {net} ===")
        input_infos = hef.get_input_vstream_infos(net)

        for info in input_infos:
            print(f"  ➤ Input name : {info.name}")
            print(f"    Shape      : {info.shape}")
            print("")


def main():
    args = parse_args()
    inspect_hef(args.hef, args.net)


if __name__ == "__main__":
    main()
