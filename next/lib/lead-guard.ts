/**
 * Client-side spam defenses for landing page forms. Mirrors /js/lead-form.js
 * on the static site so every form applies the same rules.
 */

export const HONEYPOT_NAME = "company_website";
export const MIN_SUBMIT_MS = 2800;

// +1 area codes that belong to Canada and the Caribbean, not the US.
const NON_US = new Set(
  (
    "204 226 236 249 250 257 263 289 306 343 354 365 367 368 382 387 403 416 418 428 431 437 438 450 460 468 474 " +
    "506 514 519 548 579 581 584 587 604 613 639 647 672 683 705 709 742 753 778 780 782 807 819 825 867 873 879 " +
    "902 905 942 242 246 264 268 284 345 441 473 649 658 664 721 758 767 784 809 829 849 868 869 876"
  ).split(" "),
);

export function isUsPhone(phone: string): boolean {
  const raw = phone.trim();
  if (!raw || /[a-z]/i.test(raw)) return false;
  if (raw.startsWith("+") && !/^\+\s*1(\D|$)/.test(raw)) return false;
  let digits = raw.replace(/\D/g, "");
  if (/^(011|00)/.test(digits)) return false;
  if (digits.length === 11 && digits.startsWith("1")) digits = digits.slice(1);
  if (digits.length !== 10) return false;
  const area = digits.slice(0, 3);
  const exchange = digits.slice(3, 6);
  if (!/^[2-9]\d\d$/.test(area) || /^[2-9]11$/.test(area)) return false;
  if (!/^[2-9]\d\d$/.test(exchange) || /^[2-9]11$/.test(exchange)) return false;
  if (NON_US.has(area)) return false;
  if (/^(\d)\1{9}$/.test(digits) || digits === "1234567890") return false;
  if (exchange === "555" && /^01\d\d$/.test(digits.slice(6))) return false;
  return true;
}

function vowelRatio(str: string): number {
  const letters = (str.match(/[a-z]/gi) || []).length;
  if (!letters) return 0;
  return (str.match(/[aeiou]/gi) || []).length / letters;
}

export function looksGibberishName(name: string): boolean {
  const cleaned = name.replace(/\s+/g, " ").trim();
  if (cleaned.length < 2) return true;
  const lettersOnly = cleaned.replace(/[^a-z]/gi, "");
  if (lettersOnly.length < 2) return true;
  if (lettersOnly.length >= 8 && vowelRatio(lettersOnly) < 0.18) return true;

  const parts = cleaned.split(" ").filter(Boolean);
  if (parts.length >= 2) {
    let gibberishParts = 0;
    for (const part of parts) {
      const p = part.replace(/[^a-z]/gi, "");
      if (p.length < 2) continue;
      const vr = vowelRatio(p);
      const hasRareCluster = /[bcdfghjklmnpqrstvwxyz]{5,}/i.test(p) || /[xqzjk]{2,}/i.test(p);
      if ((p.length >= 5 && vr < 0.2) || (p.length >= 6 && hasRareCluster && vr < 0.28)) gibberishParts++;
    }
    if (gibberishParts >= 2) return true;
  } else if (lettersOnly.length >= 8 && vowelRatio(lettersOnly) < 0.22) {
    return true;
  }

  return /(.)\1{3,}/i.test(lettersOnly);
}

export function isDisposableEmail(email: string): boolean {
  return /@(mailinator|guerrillamail|tempmail|10minutemail|yopmail|trashmail)\./i.test(email);
}

type GuardInput = {
  honeypot: string;
  startedAt: number;
  interacted: boolean;
  name: string;
  email: string;
  phone: string;
};

/** "bot" means drop silently; a string is a message to show the visitor; null means OK. */
export function checkLead(input: GuardInput): "bot" | string | null {
  if (input.honeypot.trim()) return "bot";
  if (!input.startedAt || Date.now() - input.startedAt < MIN_SUBMIT_MS) return "bot";
  if (!input.interacted) return "bot";
  if (looksGibberishName(input.name)) return "Please enter your real first and last name.";
  if (!isUsPhone(input.phone)) {
    return "Please enter a valid US phone number. We are not able to accept international numbers.";
  }
  if (isDisposableEmail(input.email)) return "Please use a permanent work or personal email address.";
  return null;
}
