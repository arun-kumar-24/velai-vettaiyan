from langchain_ollama import ChatOllama

class JobAnalyzer:
    def __init__(self, user_prefs):
        self.llm = ChatOllama(model="llama3.2")
        self.user_prefs = user_prefs

    def analyze_job(self, job_data):
        """
        Analyzes the job to determine a relevance score (0-100).
        job_data: [id, title, company, location, stipend, duration, type, skills, link]
        """
        job_text = f"""
        Role: {job_data[1]}
        Company: {job_data[2]}
        Location: {job_data[3]}
        Stipend: {job_data[4]}
        Skills: {job_data[7]}
        Type: {job_data[6]}
        """

        prompt = f"""
        You are a job relevance scorer. 
        User Preferences: {self.user_prefs}
        
        Job Details:
        {job_text}
        
        Task: rate this job from 0 to 100 based on how well it matches the user's preferences.
        Consider Role title matches, Skills overlap, Location, and Stipend.
        
        Output strictly only the number (e.g., 85). Do not output any text.
        """
        
        try:
            response = self.llm.invoke(prompt)
            # Invoke returns a message object or string depending on version, 
            # assuming .content for AIMessage or string directly.
            content = response.content if hasattr(response, 'content') else str(response)
            score = int(''.join(filter(str.isdigit, content)))
            return min(100, max(0, score))
        except Exception as e:
            print(f"[-] LLM Error (Score): {e}")
            return 0

    def should_email(self, job_data, score):
        """
        Asks LLM if we should email the user about this high-scoring job.
        """
        # Note: This method doesn't explicitly use user_prefs but the decision might benefit from it.
        # For now, keeping it as is, just using score and job details.
        
        prompt = f"""
        The following job scored {score}/100 for the user.
        Job: {job_data[1]} at {job_data[2]}
        Skills: {job_data[7]}
        
        Should I send an email notification to the user?
        Reply strictly with 'YES' or 'NO'.
        """
        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            return "YES" in content.upper()
        except:
            return False
