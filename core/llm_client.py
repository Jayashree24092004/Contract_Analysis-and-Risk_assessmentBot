class LLMClient:
    def __init__(self, provider: str, api_key: str | None = None):
        self.provider = provider
        self.api_key = api_key
        self.enabled = bool(api_key)

    # ------------------ Generic Chat ------------------

    def chat(self, prompt: str) -> str:
        """
        ChatGPT-like free-form response.
        Fallback-safe if no API is configured.
        """
        if not self.enabled:
            return self._demo_response(prompt)

        # TODO: integrate GPT-4 / Claude API here
        # return actual_llm_call(prompt)
        return self._demo_response(prompt)

    # ------------------ Contract Summary ------------------

    def summarize_contract(
        self,
        extracted_info: dict,
        risk_summary: dict,
        lang: str = "en"
    ) -> str:
        if not self.enabled:
            return self._demo_contract_summary(extracted_info, risk_summary, lang)

        prompt = f"""
Summarize this contract for a small business owner.
Language: {"Hindi" if lang == "hi" else "English"}

Contract type: {extracted_info.get("contract_type")}
Risk level: {risk_summary.get("level")}
Key risks: {risk_summary.get("flags")}
"""
        return self.chat(prompt)

    # ------------------ Clause Explanation ------------------

    def explain_clause(
        self,
        clause_text: str,
        risk_info: dict,
        lang: str = "en"
    ) -> str:
        if not self.enabled:
            return self._demo_clause_explanation(clause_text, risk_info, lang)

        prompt = f"""
Explain this contract clause in simple terms.
Language: {"Hindi" if lang == "hi" else "English"}

Clause:
{clause_text}

Risk: {risk_info.get("level")}
"""
        return self.chat(prompt)

    # ------------------ Alternative Clause Suggestion ------------------

    def suggest_alternative_clause(
        self,
        clause_text: str,
        risk_flags: list,
        contract_type: str
    ) -> str:
        if not self.enabled:
            return self._demo_alternative_clause(contract_type)

        prompt = f"""
Suggest a safer alternative clause for an Indian SME.
Clause:
{clause_text}

Risk flags: {risk_flags}
"""
        return self.chat(prompt)

    # ------------------ Template Generation ------------------

    def generate_template(
        self,
        contract_type: str,
        business_profile: dict
    ) -> str:
        if not self.enabled:
            return self._demo_template(contract_type)

        prompt = f"""
Generate a simple SME-friendly {contract_type} contract
Jurisdiction: India
"""
        return self.chat(prompt)

    # ------------------ Translation ------------------

    def translate_text(self, text: str, target_language: str) -> str:
        if not self.enabled:
            return text  # fallback: no translation

        prompt = f"Translate the following text to {target_language}:\n{text}"
        return self.chat(prompt)

    # ------------------ Classification ------------------

    def classify_contract_type(self, text: str) -> str:
        if not self.enabled:
            return "service"

        prompt = f"Classify the contract type:\n{text[:1000]}"
        return self.chat(prompt)

    # ================== DEMO / FALLBACK METHODS ==================

    def _demo_response(self, prompt: str) -> str:
        if "Hindi" in prompt or "हिंदी" in prompt:
            return (
                "यह क्लॉज छोटे व्यवसाय के लिए महत्वपूर्ण है। "
                "इसमें कुछ जोखिम हो सकते हैं जिन्हें समझना और आवश्यकता होने पर सुधार करना चाहिए।"
            )
        return (
            "This clause is important for a small business. "
            "It may carry certain risks that should be reviewed and improved if necessary."
        )

    def _demo_contract_summary(self, extracted_info, risk_summary, lang):
        if lang == "hi":
            return (
                f"यह एक {extracted_info.get('contract_type')} अनुबंध है। "
                f"कुल जोखिम स्तर: {risk_summary.get('level')}। "
                "कुछ शर्तों पर पुनः बातचीत की आवश्यकता हो सकती है।"
            )
        return (
            f"This is a {extracted_info.get('contract_type')} contract. "
            f"Overall risk level is {risk_summary.get('level')}. "
            "Some clauses may require renegotiation."
        )

    def _demo_clause_explanation(self, clause_text, risk_info, lang):
        if lang == "hi":
            return "यह क्लॉज व्यवसाय की जिम्मेदारियों को परिभाषित करता है और सावधानी से पढ़ा जाना चाहिए।"
        return "This clause defines business obligations and should be reviewed carefully."

    def _demo_alternative_clause(self, contract_type):
        return (
            "A balanced alternative clause may allow termination with reasonable notice "
            "and mutual obligations for both parties."
        )

    def _demo_template(self, contract_type):
        return (
            f"{contract_type.capitalize()} Agreement\n\n"
            "This agreement is made between the parties with balanced rights and obligations..."
        )
