from chatagent.core.engine.conversation import ConversationEngine
from chatagent.core.rule_based_agent import RuleBasedAgent


def test_conversation_engine_rule_based():
    scenario = ["hello", "how are you?"]
    agent = RuleBasedAgent()
    engine = ConversationEngine(agent, scenario)
    transcript = engine.run()

    expected = [
        ("env", "hello"),
        ("agent", "Hi there!"),
        ("env", "how are you?"),
        ("agent", "I'm just code, but I'm running."),
    ]

    assert transcript == expected
    assert agent.state()["history"] == [m for _, m in expected]
