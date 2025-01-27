from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
# from crewai_tools import YoutubeVideoSearchTool

from analyze_youtube_playlist.tools.youtube_playlist_scraper import YoutubePlaylistScraper
from analyze_youtube_playlist.tools.youtube_video_search import YoutubeVideoSearch

import time

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AnalyzeYoutubePlaylist():
    """AnalyzeYoutubePlaylist crew"""

    model = 'gpt-4o-mini'
    llm = LLM(model=model)

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def playlist_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['playlist_parser'],
            llm=self.llm,
            tools=[YoutubePlaylistScraper()],
            verbose=True
        )

    @agent
    def video_transcript(self) -> Agent:
        return Agent(
            config=self.agents_config['video_transcript'],
            llm=self.llm,
            tools=[YoutubeVideoSearch()],
            verbose=True
        )

    @agent
    def transcript_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['transcript_summarizer'],
            llm=self.llm,
            verbose=True
        )

    # To learn more about structured task outputs, 
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def playlist_task(self) -> Task:
        return Task(
            config=self.tasks_config['playlist_task'],
        )

    @task 
    def video_transcripts_task(self) -> Task:
        return Task(
            config=self.tasks_config['video_transcript_task']
        )
    
    @task
    def transcript_summarizer_task(self) -> Task:
        epoch_millis = str(round(time.time() * 1000)) 
        fname = f"output/transcript_summarizer_{epoch_millis}.md"

        return Task(
            config=self.tasks_config['transcript_summarizer_task'],
            output_file=fname
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AnalyzeYoutubePlaylist crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )