#!/usr/bin/env python3

import argparse
from hailo_platform import HEF


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect HEF vstreams (inputs/outputs) and metadata."
    )

    # Mandatory HEF path
    parser.add_argument(
        "hef",
        type=str,
        help="Path to HEF file (mandatory)"
    )

    # Optional network filter
    parser.add_argument(
        "--net",
        type=str,
        default=None,
        help="Inspect only a specific network name"
    )

    return parser.parse_args()


def print_info_block(title, infos, indent="  "):
    if not infos:
        print(f"{indent}(none)")
        return

    for info in infos:
        print(f"{indent}➤ {title} name : {getattr(info, 'name', '<unknown>')}")
        print(f"{indent}  Shape        : {getattr(info, 'shape', '<unknown>')}")

        # Dump any other simple attributes the info object exposes
        extra_attrs = []
        for attr in dir(info):
            if attr.startswith("_"):
                continue
            if attr in ("name", "shape"):
                continue

            try:
                value = getattr(info, attr)
            except Exception:
                continue

            if callable(value):
                continue

            # Only show "simple" values directly, to avoid noisy internal objects
            if isinstance(value, (int, float, str, bool, tuple, list, dict)):
                extra_attrs.append((attr, value))
            else:
                # Show just the type for more complex objects
                extra_attrs.append((attr, f"<{type(value).__name__}>"))

        if extra_attrs:
            print(f"{indent}  Other attributes from HEF:")
            for k, v in sorted(extra_attrs, key=lambda x: x[0]):
                print(f"{indent}    - {k}: {v}")
        print("")  # blank line between entries


def inspect_hef(hef_path, net_filter=None):
    print(f"📦 Loading HEF: {hef_path}")
    hef = HEF(hef_path)

    networks = hef.get_networks_names()
    print(f"Found {len(networks)} network(s) in HEF:")
    for n in networks:
        print(f"  • {n}")

    if net_filter and net_filter not in networks:
        print(f"\n❌ Network '{net_filter}' not found in HEF!")
        print("Available networks:")
        for n in networks:
            print("  •", n)
        return

    for net in networks:
        if net_filter and net != net_filter:
            continue

        print(f"\n============================================")
        print(f"🧠 Network: {net}")
        print(f"============================================")

        # Inputs
        try:
            input_infos = hef.get_input_vstream_infos(net)
        except TypeError:
            # Fallback to API without net argument (for single-network HEFs)
            input_infos = hef.get_input_vstream_infos()
        print("\n🔹 Input vstreams:")
        print_info_block("Input", input_infos)

        # Outputs
        try:
            output_infos = hef.get_output_vstream_infos(net)
        except TypeError:
            output_infos = hef.get_output_vstream_infos()
        print("🔸 Output vstreams:")
        print_info_block("Output", output_infos)

        # Simple summary
        print("📊 Summary:")
        print(f"  Inputs : {len(input_infos)}")
        print(f"  Outputs: {len(output_infos)}")
        print("")


def main():
    args = parse_args()
    inspect_hef(args.hef, args.net)


if __name__ == "__main__":
    main()
